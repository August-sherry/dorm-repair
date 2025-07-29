<template>
  <LayoutCenter>
    <h1 class="title">宿舍智能报修系统</h1>
    <div class="btn-group">
      <router-link to="/new"   class="btn primary">我是学生 → 去报修</router-link>
      <router-link to="/login/worker" class="btn secondary">我是维修工 → 登录</router-link>
      <router-link to="/admin/login" class="btn admin">进入后台</router-link>
    </div>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LayoutCenter from '@/components/LayoutCenter.vue'

const router = useRouter()
const adminTarget = ref('')
function goAdmin() {
  if (adminTarget.value) {
    router.push(adminTarget.value)
    adminTarget.value = ''
  }
}
</script>

<style scoped>
.title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 48px;
  color: #303133;
  text-align: center;   /* 居中 */
}
.btn-group {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 40px;
}
.btn {
  padding: 14px 48px;
  font-size: 18px;
  border-radius: 8px;
  text-decoration: none;
  color: #fff;
  transition: all 0.2s;
}
.primary   { background: #409eff; }
.secondary { background: #67c23a; }
.admin-box {
  font-size: 18px;
  color: #606266;
  text-align: center;   /* 居中 */
}
.admin-box select {
  margin-left: 8px;
  padding: 4px 8px;
  font-size: 16px;
}
</style>
