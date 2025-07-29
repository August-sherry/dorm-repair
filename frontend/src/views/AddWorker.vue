<template>
  <LayoutCenter>
    <h1 class="title">添加维修工</h1>

    <form @submit.prevent="add" class="form">
      <label>
        <span>手机号</span>
        <input v-model="phone" type="tel" required placeholder="例如：13800000000" />
      </label>

      <button type="submit" :disabled="loading" class="submit-btn">
        {{ loading ? '添加中…' : '添加维修工' }}
      </button>

      <p v-if="msg" :class="{ ok: success }">{{ msg }}</p>
    </form>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LayoutCenter from '@/components/LayoutCenter.vue'

const phone   = ref('')
const msg     = ref('')
const success = ref(false)
const loading = ref(false)
const router  = useRouter()

async function add() {
  msg.value   = ''
  success.value = false
  loading.value = true

  try {
    const res = await fetch('http://127.0.0.1:8000/admin/workers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone: phone.value.trim() })
    })

    if (res.ok) {
      msg.value   = '添加成功！'
      success.value = true
      phone.value = ''          // 清空输入框
    } else {
      const data = await res.json()
      msg.value = data.detail || '添加失败'
    }
  } catch {
    msg.value = '网络异常'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 40px;
  color: #303133;
  text-align: center;
}
.form {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  font-size: 20px;
}
.submit-btn {
  padding: 14px 0;
  font-size: 22px;
  border-radius: 8px;
  background: #67c23a;
  color: #fff;
  border: none;
  cursor: pointer;
}
.ok {
  color: green;
  text-align: center;
}
</style>
