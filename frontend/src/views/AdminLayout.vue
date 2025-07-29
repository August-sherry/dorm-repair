<template>
  <div class="admin-layout">
    <!-- 左侧导航 -->
    <nav class="sidebar">
      <router-link to="/worker" class="nav-item">接单</router-link>
      <router-link to="/kpi" class="nav-item">KPI</router-link>
      <router-link to="/list" class="nav-item">工单列表</router-link>
    </nav>

    <!-- 右侧内容 -->
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden; /* 关键：防止子内容撑高 */
}

.sidebar {
  width: 200px;
  background: #001529;
  display: flex;
  flex-direction: column;
  padding-top: 2rem;
}

.nav-item {
  padding: 14px 20px;
  color: #fff;
  text-decoration: none;
  transition: background 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: #1890ff;
}

.main {
  flex: 1;
  height: 100%;
  overflow: hidden; /* 让内容自己滚动 */
}
</style>
