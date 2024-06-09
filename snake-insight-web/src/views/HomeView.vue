<template>
  <el-scrollbar height="100vh">
    <nav-bar />
        <el-row>
          <el-col :lg="8" :md="10" :sm="24" class="map-col">
            <guang-zhou-map />
          </el-col>
          <el-col :lg="16" :md="14" :sm="24">
            <el-row>
              <el-col :lg="8" :md="12" :sm="24">
                <div><avg-price /></div>
              </el-col>
              <el-col :lg="8" :md="12" :sm="24">
                <!-- TODO: 获取选择区域-->
                <div><space-price :region="'越秀'"/></div>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
  </el-scrollbar>
</template>

<script setup>
</script>

<style scoped>
/* .map-col{
  margin: 0 40px;
  height: 640px;
} */
</style>