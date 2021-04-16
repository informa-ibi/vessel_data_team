# Notes

#### Conflicts
Unique combinations for conflict status and ignore reason (excluding pending 
conflicts):

    df_conflicts_resolved[['CONFLICT_STATUS', 'IGNORE_REASON']].drop_duplicates()
    
          CONFLICT_STATUS         IGNORE_REASON
    1             IGNORED              Likeness
    13            IGNORED   Conflict with Other
    40            IGNORED       Old Information
    52      MANUAL UPDATE                   NaN
    63            IGNORED  Regenerated Conflict
    161           IGNORED             Incorrect
    245     IGNORED VALUE              Likeness
    504           IGNORED     Update of History
    1532          IGNORED                   NaN
    5597          IGNORED         Manual Update
    6538          IGNORED   Conflict with Class
    11731         IGNORED          Does not fit
    46960         IGNORED                 Other
    
They are not always clearly meaning that the source value is correct, for example
'Regenerated Conflict' could be that the conflict is has been manually updated or
ignored before.

The data will be filtered to the following, when checking the feed could be correct:

          CONFLICT_STATUS         IGNORE_REASON
    1             IGNORED              Likeness
    52      MANUAL UPDATE                   NaN
    245     IGNORED VALUE              Likeness
    1532          IGNORED                   NaN
    5597          IGNORED         Manual Update
    
Some of the ignore reasons do not explicitly infer that the conflict was correct, but 
these cases were reviewed and if removed from the above subset - it was since the 
conflicts in that subgroup were deemed as incorrect.
   
Checking which feed supplies the correct information first when some of the
feeds where updated/created/resolved at the same time - include both as first.

To decide:

- Some vessels only have one conflict but it is resolved as 'IGNORED - Likeness' 
which suggests the information has already been updated before the feed. Do we
include these?
- Also sometimes the first reporting feed is resolved as likeness - others may be resolved
first but only looking at the reporting pattern - or they could have been updated manually 
before

Removing duplicate conflicts per vessel using the following methods:

    df_vessel.drop_duplicates(subset=['DATA_FEED', 'DB_VALUE'])\
    .drop_duplicates(subset=['DATA_FEED', 'SOURCE_VALUE'])

As the conflict from the same feed (if with a slightly different
source value) will be recreated and can be removed and equally with the same
value from the same feed at a later date can be removed.