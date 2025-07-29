<template>
  <div class="center-shell">
    <slot />
  </div>
</template>

<style scoped>
.center-shell {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 4rem 1rem 2rem;
  box-sizing: border-box;
  background: #f5f7fa;
  overflow-y: auto; /* 内容过多时在内部滚动 */
}
</style>
