# coding=utf-8
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from .barbase import bar_base,charts_base,bar_test
from django.shortcuts import render
from .table import table



# Create your views here.


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


sql = """select IFNULL(number,0) as anumber,IFNULL(name,"没有选择模块") as module,c.id FROM (
            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0'  and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='40'
            GROUP BY zm.car) as a 
            LEFT JOIN(select name,id from zt_module where root='{0}' and parent='0' and deleted='0' ) as b
            on a.car = b.id

            union

            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0' and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product = '{0}' and zb.project='40'
            GROUP BY zm.car) as a 
            RIGHT  JOIN(select name as modulename ,id from zt_module where root='{0}' and parent='0' and deleted='0' and (type='bug' or type='story')) as b
            on a.car = b.id
            ) as c  
            group by module
            """

sqlmodulesum = """
    select a.number,replace(name,'云苍穹-','') AS rep,a.id
    from (SELECT count(1) as number,zp.name,zp.id FROM zt_bug zb
    LEFT JOIN zt_product zp
    on zb.product=zp.id
    where zp.line='{}' and zb.project='40' 
    GROUP BY zp.name) as a
    ORDER BY rep
    """


sqlmodule = """
    select name from zt_module where id= '{}'
    """

sqlproduct ="""select name from  zt_product where id ='{}'"""


sqldate = """
     SELECT
        COUNT( 1 ) AS number,
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) AS datenumber,
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) AS id 
    FROM
        zt_bug 
    WHERE
        project = '40' 
        AND DATE_FORMAT( openedDate, '%Y-%m-%d' ) >= '2021-10-18'  and WeekDay(openedDate)   between 0 and 4
    GROUP BY
        DATE_FORMAT( openedDate, '%Y-%m-%d' ) 
    ORDER BY
        openedDate
    
    
 """

sqltoday ="""
            select IFNULL(number,0) as anumber,IFNULL(name,"无") as module,c.id FROM (
            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                   zt_module as a  where a.root='{0}' and a.deleted='0'  and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='40' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            LEFT JOIN(select name,id from zt_module where root={0} and parent='0' and deleted='0' ) as b
            on a.car = b.id


            union

            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0' and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='40' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            RIGHT  JOIN(select name as modulename ,id from zt_module where root='{0}' and parent='0' and deleted='0' and (type='bug' or type='story') ) as b
            on a.car = b.id
            ) as c 
            ORDER BY module
"""
sqlproducttoday="""
    SELECT  IFNULL(btemp.number,0) as number,replace(atemp.name,'云苍穹-','')as name,atemp.id from (
    select zp.id,zp.name from zt_product zp 
    inner JOIN zt_projectproduct as zpp on zp.id =zpp.product
    where zpp.project='40' and zp.line ='{0}') as atemp
    LEFT JOIN
    (
    
    SELECT
        zp.name,count(1) as number,zp.id
    FROM
        zt_product zp
        inner  JOIN zt_projectproduct zpp ON zp.id = zpp.product
        inner  JOIN zt_bug zb ON zb.product = zp.id 
    WHERE
        zpp.project = '40' 
        AND zp.line = '{0}' 
        AND DATE_FORMAT( zb.openedDate, '%Y-%m-%d' ) = CURDATE( )
        GROUP BY zp.name
        ) as btemp
        on atemp.id = btemp.id
        ORDER BY name
"""
sqlmoduletoday = """
select IFNULL(number,0) as anumber,IFNULL(name,"无") as module,c.id FROM (
            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                   zt_module as a  where a.root='{0}' and a.deleted='0'  and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}' and zb.project='40' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            LEFT JOIN(select name,id from zt_module where root=22 and parent='0' and deleted='0' ) as b
            on a.car = b.id


            union

            select a.number,b.* from(select zm.car,zm.parent,zm.name,COUNT(1) as number from zt_bug zb
            LEFT JOIN (SELECT
                    SUBSTRING_INDEX( SUBSTRING_INDEX(path, ',', 2) ,',',-1) AS car,
                    a.*
            FROM
                    zt_module as a  where a.root='{0}' and a.deleted='0' and (a.type ='bug' or a.type ='story')
            ) as zm
            on zb.module = zm.id
            where zb.product ='{0}'and zb.project='40' and DATE_FORMAT(zb.openedDate,'%Y-%m-%d') = CURDATE()
            GROUP BY zm.car) as a 
            RIGHT  JOIN(select name as modulename ,id from zt_module where root='{0}' and parent='0' and deleted='0' and (type='bug' or type='story') ) as b
            on a.car = b.id
            ) as c  
            ORDER BY module
            """
progresssql ="""
    select AVG(number)as num from zt_progress where line ='{0}'
"""

projectsql="""select number from zt_progress where id ='{0}'"""

class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        moduleid = (kwargs["moduleid"])
        print(moduleid)
        return JsonResponse(json.loads(bar_base(sqlproduct.format(moduleid),sql.format(moduleid),projectsql.format(moduleid),sqltoday.format(moduleid))))


# class ChartView(APIView):
#     def get(self, request, *args, **kwargs):
#         moduleid = (kwargs["moduleid"])
#         # print(json.loads(bar_base(sql.format(moduleid,moduleid,moduleid,moduleid,moduleid,moduleid))))
#         data = JsonResponse(json.loads(bar_base(sql.format(moduleid,moduleid,moduleid,moduleid,moduleid,moduleid),sqlmodule.format(moduleid))))
#         return render(request,"index6.html",data)


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/index8.html",encoding="utf-8").read())


class CultivatesView(APIView):
    def get(self, request, *args, **kwargs):
        moduleid = (kwargs["moduleid"])
        return JsonResponse(json.loads(bar_base(sqlmodule.format(moduleid),sqlmodulesum.format(moduleid),progresssql.format(moduleid),sqlproducttoday.format(moduleid))))



class ModuleView(APIView):
    def get(self, request, *args, **kwargs):
        data = charts_base(sqldate)
        return JsonResponse(json.loads(data))

sql1_test="""
    select number,name,id from t_test
    """
sql2_test="""
    select dataline,name,id from t_test
"""
sql3_test = """select number1,name,id from t_test"""
sql4_test = """select number2,name,id from t_test"""
sql5_test = """select number3,name,id from t_test"""

class ModuleTestView(APIView):
    def get(self, request, *args, **kwargs):
        data = bar_test(sql2_test,sql1_test,sql3_test,sql4_test,sql5_test)
        return JsonResponse(json.loads(data))



# class LiquidView(APIView):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(json.loads(liquid_test))

