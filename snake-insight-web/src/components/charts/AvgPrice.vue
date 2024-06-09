<template>
    <div class="avg-price" style="width: 100%;height: 40vh;"></div>
</template>

<script lang="ts" setup>
import type {SnachResponse} from "@/scripts/Responce";

const options = reactive({
    title: {
        text: '各区平均价格'
    },
    tooltip: {},
    legend: {},
    dataset: {
        // 提供一份数据。
        source: [
            ['行政区', '平均租房价格'],
            ['越秀区', 43.3],
            ['海珠区', 83.1],
            ['天河区', 86.4],
            ['白云区', 72.4],
            ['黄埔区', 72.4],
            ['番禺区', 72.4],
            ['花都区', 72.4],
            ['南沙区', 72.4],
            ['增城区', 72.4],
            ['从化区', 72.4]
        ]
    },
    // 声明一个 X 轴，类目轴（category）。默认情况下，类目轴对应到 dataset 第一列。
    xAxis: { type: 'category' },
    // 声明一个 Y 轴，数值轴。
    yAxis: {},
    // 声明多个 bar 系列，默认情况下，每个系列会自动对应到 dataset 的每一列。
    series: [{ type: 'bar' }]
})

function  getDataSetSource() {
  console.log(import.meta.env)
  // MESSAGE 传递Json格式数据要用POST方法
  $.post({
    url: import.meta.env.VITE_API_BASE_URL+'/plot',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify({
      "loc": ["广州"],
      "x": "space",
      "ys": [["price", "Box"]],
      "detailed": true
    }),
    success: (data: SnachResponse<Object>) => {
      // TODO onSuccess
      // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
      // MESSAGE 所以理论上不要用这个interface
      console.log(data)
    }
  })
}
function initMap() {
    getDataSetSource()
    let avgPrice = echarts.init($('.avg-price').get(0))
    avgPrice.showLoading()
    avgPrice.setOption(options)
    avgPrice.hideLoading()
    window.addEventListener('resize', () => {
        avgPrice.resize()
    })
}


onMounted(() => {
    setTimeout(() => {
        initMap()
    }, 20)
})
</script>