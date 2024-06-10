<template>
  <el-scrollbar height="100vh">
    <nav-bar />
        <el-row>
          <el-col :lg="8" :md="10" :sm="24" class="map-col">
            <guang-zhou-map @guangzhou-map-click="changeRegion"/>
          </el-col>
          <el-col :lg="16" :md="14" :sm="24">
            <el-row>
              <el-col :lg="8" :md="12" :sm="24">
                <div><avg-price /></div>
              </el-col>
              <el-col :lg="8" :md="12" :sm="24">
                <!-- TODO: 获取选择区域-->
                <div><space-price :region="curRegion.value"/></div>
              </el-col>
              <el-col :lg="8" :md="12" :sm="24">
                <div><area-price :region="curRegion.value"/></div>
              </el-col>
            </el-row>
            <el-row>
              <el-col :lg="24" :md="24" :sm="24">
                <div><room-amount-price :region="curRegion.value"/></div>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
  </el-scrollbar>
</template>

<script setup>
const curRegion = ref('天河')
function changeRegion(region) {
  console.log(region)
  curRegion.value = region.name.slice(0,-1)
  console.log(curRegion.value)
}
</script>

<style scoped>
/* .map-col{
  margin: 0 40px;
  height: 640px;
} */
</style>