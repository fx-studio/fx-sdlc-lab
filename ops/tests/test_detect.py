"""Unit tests for scripts/detect.py (playbook Stage 6: the detection script is version-controlled and unit-tested).

Run: python3 -m unittest discover -s ops/tests
Three kinds of case (lesson from SDLC-4/5: test a checker on what must pass, what must fire, and a correct case of another shape):
rarely fires on normal noise, fires on a spike, fires on a slow drift that never crosses 3 sd.
"""
import random, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from detect import judge  # noqa: E402

CFG = {"window": 14, "tail": 3, "min_points": 10, "fixed": {"smooth": 1, "levels": [[0.03, 1], [0.05, 2], [0.08, 3]]}}


def noise(n, seed=7, mu=0.01, sd=0.004):
    r = random.Random(seed)
    return [max(0.0, r.gauss(mu, sd)) for _ in range(n)]


class Quiet(unittest.TestCase):
    def test_normal_noise_rarely_reaches_level_2(self):
        # 1000 different days of plain noise, judged one by one. Run rules on pure noise DO fire sometimes: measured
        # 2026-11-10, 15 of 1000 reached level 2 or 3 (WE2 9, WE1 4, WE4 3). That is the false-alarm rate a team tunes
        # with dismissals (step 6). The test pins it under 3 %, it does not pretend it is 0.
        fired = 0
        for seed in range(1000):
            level, mode, *_ = judge(noise(20, seed), CFG)
            self.assertEqual(mode, "stats")
            fired += level >= 2
        self.assertLessEqual(fired, 30, fired)

    def test_flat_zero_baseline_has_no_statistics(self):
        level, mode, rules, mean, sd, n = judge([0.0] * 30, {**CFG, "fixed": {"smooth": 3, "levels": [[0.0001, 1], [0.2, 2], [0.4, 3]]}})
        self.assertEqual((level, mode, sd), (0, "fixed", 0.0))
        self.assertIn("sd is 0", rules[0])


class Fires(unittest.TestCase):
    def test_spike_is_level_3(self):
        level, mode, rules, *_ = judge(noise(20) + [0.09], CFG)
        self.assertEqual((level, mode), (3, "stats"))
        self.assertTrue(any(r.startswith("WE1") for r in rules))

    def test_flat_zero_then_failures_use_fixed_thresholds(self):
        cfg = {**CFG, "fixed": {"smooth": 3, "levels": [[0.0001, 1], [0.2, 2], [0.4, 3]]}}
        self.assertEqual(judge([0.0] * 30 + [0.25, 0.25, 0.25], cfg)[:2], (2, "fixed"))
        self.assertEqual(judge([0.0] * 30 + [0.5, 0.5, 0.25], cfg)[:2], (3, "fixed"))


class Floor(unittest.TestCase):
    # PR 8: days 19-20 of the baseline fired level 3 on noise (4.3 % and 3.5 % against a 1 % baseline). A floor keeps them at level 1
    # and must not hide a real incident (the 12-14 % import failures measured before the demo).
    def test_rare_noise_under_the_floor_is_only_logged(self):
        level, _, rules, *_ = judge(noise(20) + [0.043], {**CFG, "min_value": 0.05})
        self.assertEqual(level, 1)
        self.assertTrue(any("min_value" in r for r in rules))

    def test_a_real_incident_above_the_floor_still_fires(self):
        self.assertEqual(judge(noise(20) + [0.12], {**CFG, "min_value": 0.05})[0], 3)


class OtherShape(unittest.TestCase):
    def test_slow_drift_below_3_sd_is_caught(self):
        # Every point stays under mean + 3 sd, so a single-threshold alarm would never fire; WE4 does.
        base = noise(14, seed=3)
        mean = sum(base) / len(base)
        drift = [mean + 0.0008 * (i + 1) for i in range(8)]
        level, _, rules, m, sd, _ = judge(base + drift, {**CFG, "tail": 8})
        self.assertTrue(all(x < m + 3 * sd for x in drift))
        self.assertGreaterEqual(level, 2)
        self.assertTrue(any(r.startswith("WE4") for r in rules), rules)


if __name__ == "__main__":
    unittest.main()
