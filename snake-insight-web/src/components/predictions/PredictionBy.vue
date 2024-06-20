<template>
  <el-form :rules="editRules" ref="predictionFormRef" :model="req" class="prediction-form" label-position="left"
    label-width="100px">
    <el-form-item label="预算月租" prop="price" v-if="props.predict_by_type === 0">
      <div style="display:flex;">
        <el-input-number v-model.number="req.price" :min="0"/>
        <span style="margin-left: 10px;">元</span>
      </div>
    </el-form-item>
    <el-form-item label="租房面积" prop="space" v-else>
      <div style="display:flex;">
        <el-input-number v-model.number="req.space" :min="0"/>
        <span style="margin-left: 10px;">㎡</span>
      </div>
    </el-form-item>
    <el-form-item label="位置">
      <div style="display: flex;">
        <el-input class="contribute-to-selection" v-model="props.region" placeholder="全市" remote-show-suffix disabled>
        </el-input><span style="margin-left: 10px;">区</span>
        <el-select class="contribute-to-selection" v-model="req.area" filterable reserve-keyword placeholder="全区"
          no-data-text="暂无匹配的地段" no-match-text="暂无匹配的地段" default-first-option remote-show-suffix
          style="margin-left: 10px;">
          <el-option v-for="item in areaSelector.options" :key="item" :label="item" :value="item">
            <span style="float: left">{{ item }}</span>
          </el-option>
          <template #loading>
            <svg class="circular" viewBox="0 0 50 50">
              <circle class="path" cx="25" cy="25" r="20" fill="none" />
            </svg>
          </template>
        </el-select>
      </div>
    </el-form-item>
    <el-form-item label="租房楼层" prop="floor">
      <div style="display: flex;">
        <el-input-number v-model.number="req.floor"/>
        <span style="margin-left: 10px;">层</span>
      </div>
    </el-form-item>
    <el-form-item label="是否有电梯" prop="has_elevator">
      <el-switch v-model="req.has_elevator" />
    </el-form-item>

    <el-form-item label="户型规格" prop="bedroom">
      <div style="display: flex;">
        <el-input-number v-model.number="req.bedroom" :min="0"/><span style="margin: 0 10px;">室</span>
        <el-input-number v-model.number="req.living_room" :min="0"/><span style="margin-left: 10px;">厅</span>
      </div>
    </el-form-item>
  </el-form>

  <el-row>
    <div style="display: flex;align-items: center;">
      <el-button type="primary" @click="handlePredictClicked" style="width: 80px; margin: 0 12px 0 26px;">预测</el-button>
      <el-input class="result-text" v-model="predictionRes" />
      <span>{{ unit }}</span>
    </div>
  </el-row>

</template>
<script setup lang="ts">

import type { FormInstance, FormRules } from "element-plus";

const predictionFormRef = ref<FormInstance>()
const props = defineProps({
  region: { // 区域名称：['海珠', '从化', '南沙', '增城', '天河', '广州周边', '番禺', '白云', '花都', '荔湾', '越秀', '黄埔']
    type: String,
    default: ''
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
  area: '',
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
    { validator: priceValidator, trigger: 'blur' },
  ],
  space: [
    { validator: spaceValidator, trigger: 'blur' },
  ],
  floor: [
    { validator: floorValidator, trigger: 'blur' },
  ],
  living_room: [
    { validator: livingRoomValidator, trigger: 'blur' },
  ],
  bedroom: [
    { validator: bedroomValidator, trigger: 'blur' },
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
  if (props.region) {
    getAreaByRegion(props.region)
  } else {
    areaSelector.options = []
  }
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
  padding-right: 5px;
}

.unit-text {
  vertical-align: middle;
}

.room-type {
  margin: 10px;
}
</style>