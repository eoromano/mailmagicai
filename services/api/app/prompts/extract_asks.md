# Extract Asks

Extract only the concrete asks that matter.

Goals:
- identify explicit and high-confidence implicit asks
- classify each ask into the allowed `askType` values
- surface likely missing replies and blockers

Rules:
- prefer precision over recall
- do not include vague discussion as an ask
- return valid JSON only
