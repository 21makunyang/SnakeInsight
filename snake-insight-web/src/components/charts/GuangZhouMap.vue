<template>
    <div class="guangzhou-map" style="width: 100%; height: 100vh;"></div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import * as echarts from 'echarts'
import getGuangZhouMap from '@/json/getGuangZhouMap.ts'

onMounted(() => {
    let guangzhouMap = echarts.init($('.guangzhou-map').get(0))
    guangzhouMap.showLoading()
    getGuangZhouMap.then((data) => {
        guangzhouMap.hideLoading()
        echarts.registerMap('guangzhou', data)
        guangzhouMap.setOption({
            series: [
                {
                    type: 'map',
                    map: 'guangzhou'
                }
            ]
        })
    })
})

</script>