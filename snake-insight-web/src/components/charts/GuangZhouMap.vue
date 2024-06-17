<template>
    <el-radio-group v-model="graph_info" >
      <el-radio-button label="出租房数量（套）" value="count" />
      <el-radio-button label="平均价格（元）" value="avg-price" />
    </el-radio-group>
    <div class="guangzhou-map" style="width: 100%;height: 80vh;"></div>
</template>

<script lang="ts" setup>
import guangzhou from '@/json/geojson/440100.json'
const emit = defineEmits(['guangzhouMap-click'])
const graph_info = ref("count")
let guangzhouMap: any = undefined
const options = reactive(
    {
        dataset: {
            source: [

            ]
        },
        geo: {
            map: 'guangzhou',
            zoom: 1.0,
            animateDurationUpdate: 0,
            roam: true,
            label: {
                show: true,
                fontSize: 12,
                color: '#000',
            },
            itemStyle: {
                areaColor: '#fff',
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 12,
                    color: '#000',
                },
                itemStyle: {
                    areaColor: '#fff',
                    borderWidth: 2,
                },
            },
            select: {
                label: {
                    show: true,
                    fontSize: 12,
                    color: '#000',
                },
                itemStyle: {
                    areaColor: '#fff',
                    borderWidth: 2,
                },
            },
        },
        visualMap: {
            min: 0,
            max: 1000,
            left: 'left',
            top: 'bottom',
            calculable: true,
            inRange: {
                color: ['#313695',
                    '#4575b4',
                    '#74add1',
                    '#abd9e9',
                    '#e0f3f8',
                    '#ffffbf',
                    '#fee090',
                    '#fdae61',
                    '#f46d43',
                    '#d73027',
                    '#a50026'],
            },
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b} : {c}',
        },
        series: [
            {
                type: 'map',
                map: 'guangzhou',
                geoIndex: 0,
            },
        ]
    })


function getDataSetSource_count() {
    guangzhouMap.showLoading()
    // console.log(import.meta.env)
    // MESSAGE 传递Json格式数据要用POST方法
    $.post({
        url: import.meta.env.VITE_API_BASE_URL + '/plot',
        // MESSAGE Json的编码格式
        contentType: 'application/json',
        async: true,
        // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
        data: JSON.stringify({
            "loc": [`广州`],
            "x": "region",
            "ys": [["id", "Count"]],
            "detailed": true
        }),
        success: (data: any) => {
            // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
            // MESSAGE 所以理论上不要用这个SnachResponse
            const plotDict = data.plotData[0].value
            options.dataset.source = [['出租数量(套)', '行政区']]
            let max = 0
            for (const plotDictKey in plotDict) {
                options.dataset.source.push([plotDictKey === "广州周边" ? plotDictKey:plotDictKey + '区', plotDict[plotDictKey]])
                max = Math.max(max, plotDict[plotDictKey])
            }
            console.log(plotDict)
            options.visualMap.max = max
            guangzhouMap.hideLoading()
        }
    })
}

function getDataSetSource_avg() {
    // console.log(import.meta.env)
    // MESSAGE 传递Json格式数据要用POST方法
    guangzhouMap.showLoading()
    $.post({
        url: import.meta.env.VITE_API_BASE_URL + '/plot',
        // MESSAGE Json的编码格式
        contentType: 'application/json',
        async: true,
        // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
        data: JSON.stringify({
            "loc": [`广州`],
            "x": "region",
            "ys": [["price", "Avg"]],
            "detailed": true
        }),
        success: (data: any) => {
            // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
            // MESSAGE 所以理论上不要用这个SnachResponse
            const plotDict = data.plotData[0].value
            options.dataset.source = [['平均价格(元)', '行政区']]
            let max = 0
            for (const plotDictKey in plotDict) {
                options.dataset.source.push([plotDictKey === "广州周边" ? plotDictKey:plotDictKey + '区', plotDict[plotDictKey]])
                max = Math.max(max, plotDict[plotDictKey])
            }
            options.visualMap.max = max
            guangzhouMap.hideLoading()
        }
    })
}


function initMap() {
    guangzhouMap = echarts.init($('.guangzhou-map').get(0))
    guangzhouMap.showLoading()
    echarts.registerMap('guangzhou', (guangzhou) as any)
    guangzhouMap.setOption(options)
    guangzhouMap.hideLoading()
    guangzhouMap.on('click', (params) => {
        emit('guangzhouMap-click', params)
    })
    window.addEventListener('resize', () => {
        guangzhouMap.resize()
    })

}

watch(options, () => {
  initMap()
})

watch(graph_info, () => {
    if (graph_info.value === "count") {
        getDataSetSource_count()
    } else {
        getDataSetSource_avg()
    }
})

onMounted(() => {
  setTimeout(() => {
    initMap()
    if (graph_info.value === "count") {
        getDataSetSource_count()
    } else {
        getDataSetSource_avg()
    }
  }, 2)
})
</script>