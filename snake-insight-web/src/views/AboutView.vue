<template>
  <div class="about">
    <el-buttom>about</el-buttom>
    <e-charts id="main" :option="option"></e-charts>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script lang="ts" setup>
import { onMounted } from 'vue';
import * as echarts from 'echarts';

const option = {
  title: {
    text: 'ECharts 入门示例'
  },
  tooltip: {},
  legend: {
    data: ['销量']
  },
  xAxis: {
    data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
  },
  yAxis: {},
  series: [{
    name: '销量',
    type: 'bar',
    data: [5, 20, 36, 10, 10, 20]
  }]
};

onMounted(() => {
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  myChart.setOption(option);
});

</script>