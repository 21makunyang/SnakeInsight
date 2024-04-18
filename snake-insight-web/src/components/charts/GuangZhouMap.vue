<template>
    <div class="guangzhou-map" style="width: 100vh; height: 100vh;"></div>
</template>

<script lang="ts" setup>
import guangzhou from '@/json/geojson/all.json'

onMounted(() => {
    let guangzhouMap = echarts.init($('.guangzhou-map').get(0))
    guangzhouMap.showLoading()
    echarts.registerMap('guangzhou', (guangzhou) as any)
    guangzhouMap.setOption({
        geo: {
            map: 'guangzhou',
            zoom: 1.2,
            animateDurationUpdate: 0,
            roam: true,
        },
        series: [
            {
                type: 'map',
                map: 'guangzhou',
                geoIndex: 0,
            }
        ]
    })
    guangzhouMap.hideLoading()
})

</script>