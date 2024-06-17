<template>
    <div class="nav-bar">
        <div style="margin: 0 20px;">
            <el-text class="nav-title">广州租房数据分析</el-text>
        </div>
        <el-menu mode="horizontal" class="nav-menu" style="margin: 0 20px;" :ellipsis="false" :default-active="activeIndex" router>
            <div class="flex-grow"></div>
            <el-menu-item index="home" class="nav-menu-option">数据展示</el-menu-item>
            <el-menu-item index="predictionBySpace" class="nav-menu-option">房型预估</el-menu-item>
            <el-menu-item index="predictionByPrice" class="nav-menu-option">价格估计</el-menu-item>
        </el-menu>
    </div>

</template>

<script setup>
const router = useRouter();
const activeIndex = ref(document.location.pathname.split('/')[1] || 'home');
</script>

<style scoped>
.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.nav-title {
    font-size: 24px;
    font-weight: bold;
}
.flex-grow {
    flex-grow: 1;
}
</style>