#-------------------------------------------------------------------------------
# Name:        module4
# Purpose:
#
# Author:      GSS5
#
# Created:     16/12/2011
# Copyright:   (c) GSS5 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#Create a user defined function

func1 = """
function HowManyActiveWL(@ParticipantID varchar(38))
RETURNS int
begin
    declare @rslt int
    set @rslt = (select count(Participant.ParticipantID)
                from ApplWaitList
                left outer join Application on Application.ApplicationID = ApplWaitList.ApplicationID
                left outer join City on City.CityID = Application.CityID
                left outer join FamilyMember on (FamilyMember.ContractID = Application.ApplicationID)
                                                          and (FamilyMember.Relation = 0)  -- Head
                left outer join Participant on Participant.ParticipantID = FamilyMember.ParticipantID
                left outer join WaitList on WaitList.WaitListID = ApplWaitList.WaitListID
                inner join ApplicationStatus on ApplicationStatus.ApplicationStatusID = Application.ApplicationStatusID
                left outer join Voucher on Voucher.ContractID = Application.ApplicationID
                where
                    (ApplWaitList.Removed is null) and (ApplicationStatus.StatusName <> 'Hold')
                    and (
                (WaitList.Type not in (0,1))
                or (Voucher.VoucherNumber is null)
                )
                and (WaitList.Active = 1)

                and (Participant.ParticipantID = @ParticipantID) )
    return @rslt
end
"""

real_code = '''
S = """ -- 2. /  Adding  GetOwnerEmailFromHqsInspection UDF
declare @First as nchar(10)

IF  EXISTS(SELECT * FROM  INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = 'GetOwnerEmailFromHqsInspection')
	SET @First = 'ALTER '
ELSE
	SET @First = 'CREATE '

declare @GetOwnerEmailFromHqsInspectionSql as nchar(3500)
set @GetOwnerEmailFromHqsInspectionSql = @First + '
	%s'

exec SP_ExecuteSQL @GetOwnerEmailFromHqsInspectionSql"""

def get_function_name(s):
    lst = s.split(' ')[:4]
    temp = lst[1]
    temp = temp.split('(')[0]
    dbos = ['dbo.','DBO.','Dbo.']
    for dbo in dbos:
        temp = temp.replace(dbo,'')
    print 'function:',temp
    return temp

def get_new_function_sql(template, function):
    function_name = get_function_name(function)
    template = template.replace('GetOwnerEmailFromHqsInspection',function_name)
    function = function.replace("'","''")
    return template %function

def get_udf(funct):
    return get_new_function_sql(S, funct)

'''

request = {}
request['func'] = func1

ns = {}
params = ['func']
for p in params:
    code = compile('%s = """%s"""' %(p, request[p]), '<string>', 'exec')
    exec code in ns

code = compile(real_code, '<string>', 'exec')
exec code in ns

code = compile('result = get_udf(func)', '<string>', 'exec')
exec code in ns

print ns['result']

