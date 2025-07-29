<template>
  <LayoutCenter>
    <h1 class="title">评价工单</h1>

    <div v-if="loading" class="tip">加载中…</div>

    <form v-else @submit.prevent="submit" class="form">
      <p class="desc">
        工单：{{ order?.description || '' }}
      </p>

      <label>
        <span>评分（1-5 星）</span>
        <select v-model="score" required>
          <option disabled value="">请选择</option>
          <option v-for="n in 5" :key="n" :value="n">{{ n }} 星</option>
        </select>
      </label>

      <label>
        <span>评语</span>
        <textarea
          v-model="comment"
          rows="4"
          placeholder="请留下您的评价"
          required
        ></textarea>
      </label>

      <button type="submit" :disabled="loading" class="submit-btn">
        {{ loading ? '提交中…' : '提交评价' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import LayoutCenter from '@/components/LayoutCenter.vue'

const route   = useRoute()
const router  = useRouter()

const order   = ref<any>(null)
const score   = ref('')
const comment = ref('')
const loading = ref(false)
const error   = ref('')

onMounted(async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/orders/${route.params.id}`)
    order.value = await res.json()
  } catch {
    error.value = '获取工单失败'
  }
})

async function submit() {
  loading.value = true
  try {
    await fetch('http://127.0.0.1:8000/evaluations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: Number(route.params.id),
        score: Number(score.value),
        comment: comment.value.trim()
      })
    })
    alert('谢谢您的评价！')
    router.push('/list')
  } catch {
    error.value = '提交失败'
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
.desc {
  font-size: 20px;
  color: #606266;
  text-align: center;
}
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
.error {
  color: crimson;
  text-align: center;
}
</style>
