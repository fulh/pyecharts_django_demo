# coding=utf-8
from pyecharts.charts import Bar,Line,Grid,Liquid
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from .cultivates import modulebug
from pyecharts.globals import ThemeType
from pyecharts.globals import SymbolType
from .sql_util import SQLTool

import simplejson as json




def charts_base(sqlstr) -> Bar:
    color_dug = """
            function (params) {
                if (params.value > 0 && params.value < 50) {
                    return 'blue';
                } else if (params.value > 50 && params.value < 100) {
                    return 'red';
                }
                return 'green';
            }
            """
    alist = modulebug(sqlstr)

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(a["name"] for a in alist))
        .add_yaxis('总缺陷数', alist, bar_width='65%', bar_max_width='50',itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_dug)), stack="stack1")
        # .add_yaxis("今日新增", alist, bar_width='65%',bar_max_width='50', stack="stack1")
        #     .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts
        (title='云苍穹', subtitle="云苍穹-项目"),xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=25)),tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow")
                         )
        .dump_options_with_quotes()

    )
    # line = (
    #     Line()
    #         .add_xaxis(list(a["name"] for a in alist))
    #         .add_yaxis(
    #         "平均温度",
    #         list(a["value"] for a in alist),
    #         # yaxis_index=2,
    #         color="#675bba",
    #         is_smooth=True,
    #         label_opts=opts.LabelOpts(is_show=False),
    #         tooltip_opts=opts.TooltipOpts(is_show=False),
    #     )
    #
    # )
    # overlap_1 = c.overlap(line)
    # c1 = overlap_1.dump_options_with_quotes()



    # grid = (
    #     Grid()
    #     .add(overlap_1,grid_opts=opts.GridOpts(pos_right="5%"), is_control_axis_index=True)
    #     .dump_options_with_quotes()
    # )

    return c



def bar_base(sqlname,sqlline,progresssql,sqltoday=None) -> Bar:
    color_dug = """
            function (params) {
                if (params.value > 0 && params.value < 50) {
                    return 'blue';
                } else if (params.value > 50 && params.value < 100) {
                    return 'red';
                }
                return 'green';
            }
            """

    alist = modulebug(sqlline)
    modulename=modulebug(sqlname)
    todaydata = modulebug(sqltoday)
    jd = SQLTool().select_test(progresssql)



    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(a["name"] for a in alist))
        .add_yaxis("缺陷总数",alist,itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_dug)),bar_width='65%',bar_max_width='50',stack="stack1")
        # .add_yaxis("今日新增", todaydata, bar_width='65%',itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_dug)), bar_max_width='50',label_opts=opts.LabelOpts(is_show=False),stack="stack1")
        # .add_yaxis("商家c", [{"value":20,"id":"http://www.baidu.com","name":"衬衫"},{"value":20,"id":"http://www.sina.com","name":"羊毛衫"},{"value":20,"id":"http://www.yahoo.com","name":"雪纺衫"},{"value":20,"id":"http://www.baidu.com","name":"裤子"},{"value":20,"id":"http://www.baidu.com","name":"高跟鞋"},{"value":20,"id":"http://www.baidu.com","name":"袜子"}])
        .set_global_opts(title_opts=opts.TitleOpts(title=modulename[0]['value'], subtitle="云苍穹-项目"),xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=25,interval="0")),tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="shadow"))
        .dump_options_with_quotes()
    )

    # x = Faker.dogs + Faker.animal
    # xlen = len(x)
    # y = []
    # for idx, item in enumerate(x):
    #     if idx <= xlen / 2:
    #         y.append(
    #             opts.BarItem(
    #                 name=item,
    #                 value=(idx + 1) * 10,
    #                 itemstyle_opts=opts.ItemStyleOpts(color="#749f83"),
    #             )
    #         )
    #     else:
    #         y.append(
    #             opts.BarItem(
    #                 name=item,
    #                 value=(xlen + 1 - idx) * 10,
    #                 itemstyle_opts=opts.ItemStyleOpts(color="#d48265"),
    #             )
    #         )
    #
    # c = (
    #     Bar()
    #         .add_xaxis(x)
    #         .add_yaxis("series0", y)
    #         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-直方图（颜色区分）"))
    #         .dump_options_with_quotes()
    #     #     .render("bar_histogram_color.html")
    # )

    # c = (
    #     Gauge()
    #         .add(
    #         "业务指标",
    #         [("完成率", 55.5)],
    #         axisline_opts=opts.AxisLineOpts(
    #             linestyle_opts=opts.LineStyleOpts(
    #                 color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
    #             )
    #         ),
    #     )
    #         .set_global_opts(
    #         title_opts=opts.TitleOpts(title="Gauge-不同颜色"),
    #         legend_opts=opts.LegendOpts(is_show=False),
    #     ).dump_options_with_quotes()
    #
    # )



    # l1 = (
    #     Liquid()
    #         .add("进度", [jd[0]/100], center=["90%", "60%"],is_outline_show = False,)
    #         .set_global_opts(title_opts=opts.TitleOpts(title="测试进度",pos_right=50,pos_top=40,title_textstyle_opts= opts.TextStyleOpts(color="#7077ee")))
    #
    # )
    # # grid = Grid().add(l1,grid_opts=opts.GridOpts(pos_left="30%"),is_control_axis_index=True).add(c, grid_opts=opts.GridOpts(pos_right="-1%"), is_control_axis_index=True)
    # grid = Grid().add(c, grid_opts=opts.GridOpts(pos_right="20%"), is_control_axis_index=True).add(l1,grid_opts=opts.GridOpts(pos_top="50%",pos_right="75%"))
    # c1 = grid.dump_options_with_quotes()

    return c

def bar_sum(sqlname, sqlline, sqltoday=None) -> Bar:
        color_dug = """
                function (params) {
                    if (params.value > 0 && params.value < 50) {
                        return 'blue';
                    } else if (params.value > 50 && params.value < 100) {
                        return 'red';
                    }
                    return 'green';
                }
                """

        alist = modulebug(sqlline)
        modulename = modulebug(sqlname)
        todaydata=modulebug(sqltoday)

        c = (
            Bar()
                .add_xaxis(list(a["name"] for a in alist))
                .add_yaxis(modulename[0]['value'], alist, itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_dug)),
                           bar_width='65%', bar_max_width='50')
                .add_yaxis("今日新增", list(a["name"] for a in todaydata), bar_width='65%', bar_max_width='50',stack="stack1")
                # .add_yaxis("商家c", [{"value":20,"id":"http://www.baidu.com","name":"衬衫"},{"value":20,"id":"http://www.sina.com","name":"羊毛衫"},{"value":20,"id":"http://www.yahoo.com","name":"雪纺衫"},{"value":20,"id":"http://www.baidu.com","name":"裤子"},{"value":20,"id":"http://www.baidu.com","name":"高跟鞋"},{"value":20,"id":"http://www.baidu.com","name":"袜子"}])
                .set_global_opts(title_opts=opts.TitleOpts(title=modulename[0]['value'], subtitle="云苍穹-项目"),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=25)),
                                 tooltip_opts=opts.TooltipOpts(
                                     is_show=True, trigger="axis", axis_pointer_type="shadow"))
                .dump_options_with_quotes()
        )
        return c






    # filename = '养殖项目2.0-Bug.csv'
    # filepath = os.path.join(settings.MEDIA_ROOT, filename)
    # dfbug = pandas.read_csv(filepath, engine='python', encoding="gbk", index_col=False)
    # dfbug['k201'] = dfbug['所属产品'].str.split('-').str[0]
    # # data1=dfbug[dfbug['k201']=='公共'].groupby(by='所属产品').count().sort_values(by="Bug编号",ascending=False)[:10]["Bug编号"]
    # data1 = dfbug.query('k201=="繁殖"|k201=="公共"').groupby(by='所属产品').count().sort_values(by="Bug编号", ascending=False)[:20]["Bug编号"]
    #
    # a = 100
    #
    # color_dug = """
    #         function (params) {
    #             if (params.value > """ + str(a) + """) {
    #                 return 'red';
    #             }return 'green';
    #         }
    #         """
    #
    # c = (
    #     Bar()
    #         .add_xaxis(data1.index.tolist())
    #         .add_yaxis("养殖2.0缺陷统计", data1.values.tolist(), itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_dug)))
    #         .set_global_opts(
    #         title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-垂直）"),
    #         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=35)),
    #                 # datazoom_opts=opts.DataZoomOpts(orient="vertical"),
    #     ).dump_options_with_quotes()
    # )
    # return c

    # color_function = """
    #         function (params) {
    #             if (params.value > 0 && params.value < 50) {
    #                 return 'blue';
    #             } else if (params.value > 50 && params.value < 100) {
    #                 return 'red';
    #             }
    #             return 'green';
    #         }
    #         """
    # c = (
    #     Bar()
    #         .add_xaxis(Faker.choose())
    #         .add_yaxis(
    #         "商家A",
    #         Faker.values(),
    #         itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
    #     )
    #         .add_yaxis(
    #         "商家B",
    #         Faker.values(),
    #         itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
    #     )
    #         .add_yaxis(
    #         "商家C",
    #         Faker.values(),
    #         itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
    #     )
    #         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-自定义柱状颜色"))
    #         .dump_options_with_quotes()
    # )
    # return c

import random
def random_color():
     colors1 = '0123456789ABCDEF'
     num = "#"
     for i in range(6):
         num += random.choice(colors1)
     return num



def bar_test(*sql):
    sqllist =[]
    for sqlstr in sql:
        sqllist.append(modulebug(sqlstr))


    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add_xaxis(list(a["name"] for a in sqllist[0]))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            # .dump_options_with_quotes()
        )


    for i in range(0, len(sqllist)):
        c_ = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
                .add_xaxis(list(a["name"] for a in sqllist[i]))
                # .add_yaxis(columns[i], data[i])
                .add_yaxis("test"+str(i),sqllist[i],stack="stack1",itemstyle_opts=opts.ItemStyleOpts(color=random_color()),label_opts=opts.LabelOpts(position="inside"))
                # .dump_options_with_quotes()
        )
        c.overlap(c_)
    C1=c.dump_options_with_quotes()

    return C1



