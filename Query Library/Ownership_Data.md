# Current ownership (all types) for list of LLP no's

  select

  v.llpno,
  v.lregno,
  v.name,

  ro.comp_name Registered_Owner,
  co.comp_name Commercial_Operator,
  bo.comp_name Benefical_Owner, 
  tm.comp_name Technical_Manager,
  im.comp_name ISM_Manager,
  no.comp_name Nominal_Owner

  from sid.vessels v

  left join lmiuportal.vsl_owner_hist RO
  on (v.llpno=ro.llpno and ro.curr_ind='Y' and ro.owner_type='RO')

  left join lmiuportal.vsl_owner_hist CO
  on (v.llpno=co.llpno and co.curr_ind='Y' and co.owner_type='CO')

  left join lmiuportal.vsl_owner_hist BO
  on (v.llpno=bo.llpno and bo.curr_ind='Y' and bo.owner_type='BO')

  left join lmiuportal.vsl_owner_hist TM
  on (v.llpno=tm.llpno and tm.curr_ind='Y' and tm.owner_type='TM')

  left join lmiuportal.vsl_owner_hist IM
  on (v.llpno=im.llpno and im.curr_ind='Y' and im.owner_type='IM')

  left join lmiuportal.vsl_owner_hist NO
  on (v.llpno=no.llpno and no.curr_ind='Y' and no.owner_type='NO')

  where v.llpno in (1,2,3,4,284762)

  order by v.llpno;
