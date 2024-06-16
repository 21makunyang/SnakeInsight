<template>
  <el-scrollbar height="100vh">
    <nav-bar/>
    <el-row>
      <el-col :lg="8" :md="10" :sm="24" class="map-col">
        <guang-zhou-map @guangzhou-map-click="changeRegion"/>
      </el-col>
      <el-col :lg="16" :md="24" :sm="24" class="prediction-col">
        <!--预测方式：0-价格，1-面积 -->
        <prediction-by-space :region="curRegion" :predict_by_type="1"/>
      </el-col>
    </el-row>

<!--    <prediction-by-space-page/>-->
  </el-scrollbar>
</template>
<script setup lang="ts">
const curRegion = ref('白云')
function changeRegion(region) {
  // console.log(region)
  curRegion.value = region.name.slice(0, -1)
  // console.log(curRegion.value)
}
</script>

<style scoped>

</style>