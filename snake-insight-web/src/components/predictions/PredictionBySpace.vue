<template>
  <el-form :rules="editRules" ref="predictionFormRef" :model="req" class="prediction-form">
    <el-form-item label="租房价格" prop="price" v-if="props.predict_by_type === 0">
      <el-input v-model.number="req.price" placeholder="请输入租房价格"/>
    </el-form-item>
    <el-form-item label="租房面积" prop="space" v-else>
      <el-input v-model.number="req.space" placeholder="请输入租房面积"/>
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
  <el-button type="primary" @click="handlePredictClicked">预测</el-button>
  <el-input v-model="predictionRes"/>
</template>
<script setup lang="ts">

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
const priceValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('租房价格不能小于0'))
  }
}
const spaceValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('租房面积不能小于0'))
  }
}
const floorValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('租房楼层不能小于0'))
  }
}

const livingRoomValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('起居室数量不能小于0'))
  }
}
const bedroomValidator = (rule: any, value: any, callback: any) => {
  if (value < 0) {
    callback(new Error('房间数量不能小于0'))
  }
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
  if (!formEl){
    console.log('formEl is undefined')
    return
  }
  console.log('submitForm')
  formEl.validate((valid) => {
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

onMounted(() => {
  setTimeout(() => {
    getPrediction()
  }, 20)
})
</script>

<style scoped>

</style>