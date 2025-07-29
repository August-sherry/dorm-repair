<template>
  <LayoutCenter>
    <h1 class="title">管理员登录</h1>

    <form @submit.prevent="login" class="form">
      <label>
        <span>管理员口令</span>
        <input v-model="password" type="password" required />
      </label>
      <button type="submit" class="submit-btn">登录</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LayoutCenter from '@/components/LayoutCenter.vue'

const password = ref('')
const error    = ref('')
const router   = useRouter()

async function login() {
  if (password.value !== '111') {
    error.value = '口令错误'
    return
  }
  sessionStorage.setItem('admin', '1')
  router.replace('/admin/add-worker')
}
</script>

<style scoped>
.title   { font-size: 42px; margin-bottom: 40px; text-align: center; }
.form    { width: 100%; max-width: 400px; display: flex; flex-direction: column; gap: 24px; font-size: 20px; }
.submit-btn { padding: 14px 0; font-size: 22px; border-radius: 8px; background: #e6a23c; color: #fff; border: none; cursor: pointer; }
.error   { color: crimson; text-align: center; }
</style>