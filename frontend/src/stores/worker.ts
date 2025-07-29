// src/stores/worker.ts
import { defineStore } from 'pinia'

export const useWorkerStore = defineStore('worker', {
  state: () => ({
    id: 0,
    phone: ''
  }),
  actions: {
    login(id: number, phone: string) {
      this.id = id
      this.phone = phone
    }
  }
})
