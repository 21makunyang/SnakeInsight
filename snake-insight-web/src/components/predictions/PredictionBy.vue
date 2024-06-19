<template>
  <el-form :rules="editRules" ref="predictionFormRef" :model="req" class="prediction-form">
    <el-form-item label="租房价格" prop="price" v-if="props.predict_by_type === 0">
      <el-input v-model.number="req.price" placeholder="请输入租房价格"/>
    </el-form-item>
    <el-form-item label="租房面积" prop="space" v-else>
      <el-input v-model.number="req.space" placeholder="请输入租房面积"/>
    </el-form-item>
    <el-form-item label="位置">
      <el-select
          class="contribute-to-selection"
          v-model="props.region"
          filterable
          reserve-keyword
          placeholder="请输入区划"
          no-data-text="暂无匹配的区"
          no-match-text="暂无匹配的区"
          default-first-option
          remote-show-suffix
          style="width: 240px"
      >
        <el-option
            v-for="item in regionSelector.options"
            :key="item"
            :label="item"
            :value="item"
        >
          <span style="float: left">{{ item }}</span>
        </el-option>
        <template #loading>
          <svg class="circular" viewBox="0 0 50 50">
            <circle class="path" cx="25" cy="25" r="20" fill="none"/>
          </svg>
        </template>
      </el-select>
      <el-select
          class="contribute-to-selection"
          v-model="req.area"
          filterable
          reserve-keyword
          placeholder="请输入地段"
          no-data-text="暂无匹配的地段"
          no-match-text="暂无匹配的地段"
          default-first-option
          remote-show-suffix
          style="width: 240px"
      >
        <el-option
            v-for="item in areaSelector.options"
            :key="item"
            :label="item"
            :value="item"
        >
          <span style="float: left">{{ item }}</span>
        </el-option>
        <template #loading>
          <svg class="circular" viewBox="0 0 50 50">
            <circle class="path" cx="25" cy="25" r="20" fill="none"/>
          </svg>
        </template>
      </el-select>
    </el-form-item>
    <el-form-item label="租房楼层" prop="floor">
      <el-input v-model.number="req.floor" placeholder="请输入租房楼层"/>
    </el-form-item>
    <el-form-item label="是否有电梯" prop="has_elevator">
      <el-switch v-model="req.has_elevator"/>
    </el-form-item>

    <div class="room-type"><span>户型</span></div>
    <el-form-item label="房间数量" prop="bedroom">
      <el-input v-model.number="req.bedroom" placeholder="请输入房间数量"/>
    </el-form-item>
    <el-form-item label="起居室数量" prop="living_room">
      <el-input v-model.number="req.living_room" placeholder="请输入起居室数量"/>
    </el-form-item>
  </el-form>

  <el-row>
    <el-col :lg="2" :md="2" :sm="2">
      <el-button type="primary" @click="handlePredictClicked">预测</el-button>
    </el-col>
    <el-col :lg="8" :md="8" :sm="8">
      <el-input class="result-text" v-model="predictionRes"/>
    </el-col>
    <el-col :lg="8" :md="8" :sm="8"><span class="unit-text">{{ unit }}</span></el-col>
  </el-row>

</template>
<script setup lang="ts">

import type {FormInstance, FormRules} from "element-plus";

const predictionFormRef = ref<FormInstance>()
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: '天河'
  },
  predict_by_type: { // 预测方式：0-价格，1-面积
    type: Number,
    default: 0
  },
})

const region = toRef(props, 'region')
const predictionRes = ref()
const req = reactive({
  price: 0,
  space: 0,
  area: '沙太北',
  floor: 0,
  has_elevator: false,
  living_room: 0,
  bedroom: 0,
  predict_by_type: 0,
})
const unit = ref('元')
const areaSelector = reactive({
  options: []
})
const regionSelector = reactive({
  options: ['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
})
const priceValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('租房价格不能小于0'))
  }
  // 注意： 自定义校验规则必须保证每个分支都调用了callback方法
  callback()
}
const spaceValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('租房面积不能小于0'))
  }
  callback()
}
const floorValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('租房楼层不能小于0'))
  }
  callback()
}

const livingRoomValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('起居室数量不能小于0'))
  }
  callback()
}
const bedroomValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('房间数量不能小于0'))
  }
  callback()
}
const editRules = reactive<FormRules>({
  price: [
    {validator: priceValidator, trigger: 'blur'},
  ],
  space: [
    {validator: spaceValidator, trigger: 'blur'},
  ],
  floor: [
    {validator: floorValidator, trigger: 'blur'},
  ],
  living_room: [
    {validator: livingRoomValidator, trigger: 'blur'},
  ],
  bedroom: [
    {validator: bedroomValidator, trigger: 'blur'},
  ],
})

function getAreaByRegion(query: string) {
  $.post({
    url: import.meta.env.VITE_API_BASE_URL + '/getAreaByRegion',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify({
      region: region.value,
    }),
    success: (data: any) => {
      console.log(data)
      areaSelector.options = data.data.areas
    }
  })
}

function getPrediction() {

  const params = {
    ...req,
    region: props.region,
    predict_by_type: props.predict_by_type,
  }
  // console.log(params)
  $.post({
    url: import.meta.env.VITE_API_BASE_URL + '/getPrediction',
    // MESSAGE Json的编码格式
    contentType: 'application/json',
    async: true,
    // MESSAGE 传递Json格式数据时要用JSON.stringify转字符串
    data: JSON.stringify(params),
    success: (data: any) => {
      console.log(data)
      predictionRes.value = data.data.prediction
    }
  })

}

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) {
    console.log('formEl is undefined')
    return
  }
  formEl.validate((valid: boolean) => {
    console.log('valid', valid)
    if (valid) {
      console.log('submit!')
      getPrediction()
    } else {
      console.log('error submit!')
    }
  })
}

function handlePredictClicked() {
  console.log('handlePredictClicked')
  submitForm(predictionFormRef.value)
  // getPrediction()
}

watch(props, () => {
  getAreaByRegion(props.region)
})
onMounted(() => {
  setTimeout(() => {
    unit.value = props.predict_by_type === 0 ? '㎡' : '元'
    // getPrediction()
  }, 20)
})
</script>

<style scoped>
.result-text {
  margin-right: 5px;
  padding-right:5px;
}
.unit-text {
  vertical-align:middle
}
</style>