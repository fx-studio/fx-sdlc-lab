# High-risk list

A spec is **high risk** if it matches any line. High risk means the tech lead reviews it in addition to the product owner.
Quote the line that matched. If none matches, write `Risk: normal`.

1. Touches payment, authentication, or personal data leaving the user's device
2. Changes the shape of stored data (a new field, a new key, a migration)
3. Adds an external dependency (library, CDN, web service)
4. Affects more than one team
