<template>
    <div class="guangzhou-map" style="width: 100%;height: 80vh;"></div>
</template>

<script lang="ts" setup>
import guangzhou from '@/json/geojson/440100.json'
const options = reactive(
    {
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
            formatter: '{b}: {c}',
        },
        series: [
            {
                type: 'map',
                map: 'guangzhou',
                geoIndex: 0,
                data: [
                    { name: '越秀区', value: 500 },
                    { name: '荔湾区', value: 600 },
                    { name: '海珠区', value: 900 },
                    { name: '天河区', value: 1000 },
                    { name: '白云区', value: 800 },
                    { name: '黄埔区', value: 700 },
                    { name: '番禺区', value: 400 },
                    { name: '花都区', value: 300 },
                    { name: '南沙区', value: 200 },
                    { name: '增城区', value: 100 },
                    { name: '从化区', value: 100 },
                ],
            },
        ]
})
function initMap(){
    let guangzhouMap = echarts.init($('.guangzhou-map').get(0))
    guangzhouMap.showLoading()
    echarts.registerMap('guangzhou', (guangzhou) as any)
    guangzhouMap.setOption(options)
    guangzhouMap.hideLoading()
    window.addEventListener('resize', () => {
        guangzhouMap.resize()
    })

}

onMounted(() => {
    setTimeout(() => {
        initMap()
    }, 20)
})

</script>