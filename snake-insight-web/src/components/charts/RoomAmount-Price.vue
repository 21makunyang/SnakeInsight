<template>
  <div class="room-amount-price" style="width: 100%;height: 40vh;"></div>
</template>

<script lang="ts" setup>
import {watch} from "vue";

const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: ''
  }
})
let region = toRef(props, 'region')

const options = reactive({
  title: {
    text: '厅室数量-租房价格、厅室数量统计',
    // subtext: 'Fake Data',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b} : {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    // left: 'center',
    // top: 'top',
    data: [
      'rose1',
      'rose2',
      'rose3',
      'rose4',
      'rose5',
      'rose6',
      'rose7',
      'rose8'
    ]
  },
  toolbox: {
    show: false,
    feature: {
      mark: { show: true },
      dataView: { show: true, readOnly: false },
      restore: { show: true },
      saveAsImage: { show: true }
    }
  },
  series: [
    {
      name: '厅室数量-租房价格',
      type: 'pie',
      radius: ['40%', '60%'],
      center: ['35%', '50%'],
      // roseType: 'radius',
      itemStyle: {
        borderRadius: 5
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold',
          formatter: '{b} \n{c}元'
        }
      },
      data: [
        { value: 40, name: 'rose 1' },
        { value: 33, name: 'rose 2' },
        { value: 28, name: 'rose 3' },
        { value: 22, name: 'rose 4' },
        { value: 20, name: 'rose 5' },
        { value: 15, name: 'rose 6' },
        { value: 12, name: 'rose 7' },
        { value: 10, name: 'rose 8' }
      ]
    },
    {
      name: '厅室数量统计',
      type: 'pie',
      radius: [20, '60%'],
      center: ['75%', '50%'],
      roseType: 'area',
      itemStyle: {
        borderRadius: 5
      },
      data: [
        { value: 30, name: 'rose 1' },
        { value: 28, name: 'rose 2' },
        { value: 26, name: 'rose 3' },
        { value: 24, name: 'rose 4' },
        { value: 22, name: 'rose 5' },
        { value: 20, name: 'rose 6' },
        { value: 18, name: 'rose 7' },
        { value: 16, name: 'rose 8' }
      ]
    }
  ]
})

function  getDataSetSource() {
  // console.log(import.meta.env)
  // MESSAGE 传递Json格式数据要用POST方法
  $.post({
    url: import.meta.env.VITE_API_BASE_URL+'/getRoomPrice',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify({
      "region": region.value
    }),
    success: (data: any) => {
      // MESSAGE 后端返回的格式并不按照SnachResponse的格式返回
      // MESSAGE 所以理论上不要用这个interface
      if (region.value) {
        options.title.text = region.value + '区 厅室数量-租房价格、厅室数量统计'
      } else {
        options.title.text = '广州市 厅室数量-租房价格、厅室数量统计'
      }
      options.legend.data = []
      options.series[0].data = []
      options.series[1].data = []
      for (const dataKey in data.data) {
        options.legend.data.push(dataKey)
        options.series[0].data.push({ value: data.data[dataKey][0], name: dataKey })
        options.series[1].data.push({ value: data.data[dataKey][3], name: dataKey })
      }
      // console.log(data)
    }
  })
}
function initMap() {
  let avgPrice = echarts.init($('.room-amount-price').get(0))
  avgPrice.showLoading()
  avgPrice.setOption(options)
  avgPrice.hideLoading()
  window.addEventListener('resize', () => {
    avgPrice.resize()
  })
}
watch(props, () => {
  getDataSetSource()
})
watch(options, () => {
  initMap()
})

onMounted(() => {
  setTimeout(() => {
    getDataSetSource()
    initMap()
  }, 20)
})
</script>