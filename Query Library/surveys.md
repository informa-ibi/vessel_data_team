# Surveys

Use the following query for surveys:

    select t1.llpno, t3.lregno, t3.name, t1.classoc, t3.status, t2.description,  max(t1.startdt), t1.enhanced_survey_program_ind, t1.next_survey_date from sid.vslclasses t1
    left join sid.survey_type t2
    on t1.survey_type = t2.id
    left join sid.vessels t3
    on t1.llpno = t3.llpno
    where next_survey_date is not null
    and next_survey_date >= '13-JAN-2020'
    and t1.llpno = 3422
    --and status = 'L'
    group by t1.llpno, t3.lregno, t3.name, t1.classoc, t2.description, t1.enhanced_survey_program_ind, t1.next_survey_date, t3.status
    --and survey_type is not null
    --order by next_survey_date asc; 
    order by llpno;
