<template>
  <LayoutCenter>
    <h1 class="title">我要报修</h1>

    <form @submit.prevent="submit" class="form">
      <label>
        <span>宿舍号</span>
        <input
          v-model="form.room"
          type="text"
          placeholder="如：A101"
          required
        />
      </label>

      <label>
        <span>类别</span>
        <select v-model="form.category" required>
          <option disabled value="">请选择类别</option>
          <option>水管</option>
          <option>电路</option>
          <option>家具</option>
          <option>其他</option>
        </select>
      </label>

      <label>
        <span>描述</span>
        <textarea
          v-model="form.desc"
          placeholder="请描述具体问题，如漏水位置、灯泡型号等"
          rows="4"
          required
        ></textarea>
      </label>

      <button type="submit" :disabled="loading" class="submit-btn">
        {{ loading ? '提交中…' : '提交报修' }}
      </button>
    </form>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LayoutCenter from '@/components/LayoutCenter.vue'

const router = useRouter()
const loading = ref(false)
const form = ref({ room: '', category: '', desc: '' })

async function submit() {
  loading.value = true
  try {
    await fetch('http://127.0.0.1:8000/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1, // 示例
        category_id: 1, // 示例
        description: `[${form.value.room}] ${form.value.desc}`
      })
    })
    alert('报修成功！')
    router.push('/select-role')
  } catch {
    alert('提交失败')
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
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  font-size: 20px;
}
.form input,
.form select,
.form textarea {
  width: 100%;
  padding: 12px;
  font-size: 20px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
}
.submit-btn {
  padding: 14px 0;
  font-size: 22px;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
  border: none;
  cursor: pointer;
}
</style>
