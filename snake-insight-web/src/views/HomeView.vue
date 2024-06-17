<template>
  <el-scrollbar height="90vh">
    <el-row class="graph-row">
      <el-col :lg="8" :md="10" :sm="24" class="map-col">
        <guang-zhou-map @guangzhou-map-click="changeRegion"/>
      </el-col>
      <el-col :lg="16" :md="14" :sm="24">
        <el-row class="graph-row">
          <el-col :lg="8" :md="12" :sm="24">
            <div>
              <avg-price/>
            </div>
          </el-col>
          <el-col :lg="8" :md="12" :sm="24">
            <!-- TODO: 获取选择区域-->
            <div>
              <space-price :region="curRegion"/>
            </div>
          </el-col>
          <el-col :lg="8" :md="12" :sm="24">
            <el-scrollbar height="40vh">
              <div>
                <area-price :region="curRegion"/>
              </div>
            </el-scrollbar>
          </el-col>
        </el-row>
        <el-row class="graph-row">
          <el-col :lg="24" :md="24" :sm="24">
            <div>
              <room-amount-price :region="curRegion"/>
            </div>
          </el-col>
        </el-row>
        
      </el-col>
    </el-row>
    <el-row class="graph-row">
          <el-col :md="12" :sm="24">
            <div>
              <floor-price :region="curRegion" :has_elevator="true"/>
            </div>
          </el-col>
          <el-col :md="12" :sm="24">
            <div>
              <floor-price :region="curRegion" :has_elevator="false"/>
            </div>
          </el-col>
        </el-row>
    <el-row class="graph-row">
      <el-col :span="20" :offset="2">
        <div>
          <box-price :region="curRegion"></box-price>
        </div>
      </el-col>

    </el-row>
  </el-scrollbar>
</template>

<script setup>
const curRegion = ref('白云')

function changeRegion(region) {
  // console.log(region)
  curRegion.value = region.name.slice(0, -1)
  // console.log(curRegion.value)
}
</script>

<style scoped>
/* .map-col{
  margin: 0 40px;
  height: 640px;
} */
.graph-row {
  margin: 20px 20px;
}
</style>