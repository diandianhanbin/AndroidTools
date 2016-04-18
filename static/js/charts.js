/**
 * Created by SvenWeng on 16/4/12.
 */

$(document).ready(function () {
    //内存信息获取
    $('#mem_query').click(function () {
        var filename = $("#selquery").val();
        var myChart = echarts.init(document.getElementById('main'), 'dark');
        $.get('/datashow/getmemdata/' + filename).done(function (data) {
            myChart.hideLoading();
            myChart.setOption({
                title: {
                    text: '内存监控信息'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['内存总体使用量', '内存剩余可用量']
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: '内存剩余可用量',
                        type: 'line',
                        areaStyle: {normal: {}},
                        data: data['user_data']
                    },
                    {
                        name: '内存总体使用量',
                        type: 'line',
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        },
                        opacity: '0.1',
                        areaStyle: {normal: {opacity: '0.1'}},
                        data: data['total_data']
                    }
                ]
            });
        });
    });
    $("#starttool").click(function () {
        $.ajax({
            url: '/datashow/setuptools/'
        })

    });
    //cpu信息获取
    $("#cpu_query").click(function () {
        var filename = $("#selquery").val();
        var myChart = echarts.init(document.getElementById('main'), 'dark');
        $.get('/datashow/getcpudata/' + filename).done(function (data) {
            myChart.hideLoading();
            myChart.setOption({
                title: {
                    text: 'cpu监控信息'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['AppCpu总体使用量', 'AppCpu用户使用量']
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'AppCpu用户使用量',
                        type: 'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data: data['user_data']
                    },
                    {
                        name: 'AppCpu总体使用量',
                        type: 'line',
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        },
                        areaStyle: {normal: {opacity: '0.05'}},
                        data: data['total_data']
                    }
                ]
            })
        })
    });
    $("#getflow").click(function () {
        var val = $("#getflow").text();
        var myDate = new Date();
        var package_name = $("#package").val();
        if (val == '点击开始测试') {
            $("#getflow").removeClass().addClass('btn btn-danger');
            $.get(
                '/datashow/testflow/',
                {mark: 'start', package: package_name}
            );
            $("#getflow").text('点击停止测试');
            $("#start").text('开始测试时间为: ' + myDate.toLocaleTimeString());
            $("#end").text('');
            $("#result").html('')
        }
        else {
            $("#getflow").removeClass().addClass('btn btn-default');
            $("#end").text('结束测试时间为: ' + myDate.toLocaleTimeString());
            $("#getflow").text('点击开始测试');
            $.get(
                '/datashow/testflow/',
                {mark: 'end', package: package_name},
                function (data) {
                    $("#result").html(
                        "测试结果:" +
                        "<hr>" +
                        "测试一共耗时:" + data['time'] + "秒" +
                        "<hr>" +
                        "总计流量消耗: " + data['total'] + "byte" +
                        "<hr>" +
                        "上行流量: " + data['up'] + "byte" +
                        "<hr>" +
                        "下行流量: " + data['down']
                    )
                }
            );
            $("#selection").html('');
            $.ajax({
                url: '/datashow/getdirlist/flowinfo',
                success: function (data) {
                    var arr = data['data'];
                    var select = $("<select id='selquery' class='form-control'></select>");
                    for (var i = 0; i < arr.length; i++) {
                        select = select.append("<option value='" + arr[i] + "'>" + arr[i] + "</option>")
                    }
                    $("#selection").append(select)
                }
            });

        }
    });
    //流量信息获取
    $("#flow_query").click(function () {
        var filename = $("#selquery").val();
        var myChart = echarts.init(document.getElementById('main'), 'dark');
        $.get('/datashow/flowinfo/' + filename).done(function (data) {
            myChart.hideLoading();
            myChart.setOption({
                title: {
                    text: '流量监控信息'
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: ['下行流量', '上行流量']
                },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: '上行流量',
                        type: 'line',
                        stack: '总量',
                        areaStyle: {normal: {}},
                        data: data['up']
                    },
                    {
                        name: '下行流量',
                        type: 'line',
                        label: {
                            normal: {
                                show: true,
                                position: 'top'
                            }
                        },
                        areaStyle: {normal: {opacity: '0.05'}},
                        data: data['down']
                    }
                ]
            })
        })
    });
    //获取当前包名
    $("#get_cur_packagename").click(function () {
        $.getJSON(
            '/datashow/get_cur_packagename/',
            function (data) {
                $("#pkinfo").fadeIn('slow');
                $("#package_name").html('当前打开的包名为: <mark>'+data['package_name']+"</mark>");
                $("#activity_name").html('当前打开的avtivity为: <mark>'+data['avtivity_name']+"</mark>")
            }
        )
    });
    //获取所有第三方包名
    $("#get_third_packagename").click(function () {
        $.getJSON(
            '/datashow/get_third_packagename/',
            function (data) {
                $("#third_list_container").addClass("panel panel-default");
                var len = data['third_pknm'].length;
                $("#pk_list_header").text('该手机一共有'+len+'个应用');
                $.each(data['third_pknm'], function (i, val) {
                    $("#pk_list").append('<li class="list-group-item">'+val+'</li>')
                })
            }
        )
    });
});
