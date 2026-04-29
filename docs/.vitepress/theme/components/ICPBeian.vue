<script setup lang="ts">
import { ref, onMounted } from 'vue'

const beianNumber = '赣ICP备2023009313号-3'
const beianUrl = 'https://beian.miit.gov.cn/'
const showBeian = ref(false)

onMounted(() => {
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    showBeian.value = hostname.endsWith('.sdcom.top') || hostname.endsWith('.cnb.run')
  }
})
</script>

<template>
  <div v-if="showBeian" class="icp-beian">
    <a :href="beianUrl" target="_blank" rel="noopener noreferrer">
      {{ beianNumber }}
    </a>
  </div>
</template>

<style scoped>
.icp-beian {
  font-size: 12px;
  color: #999;
  text-align: center;
  padding: 8px 0;
  border-top: 1px solid #e5e7eb;
  margin-top: 16px;
}

.icp-beian a {
  color: #999;
  text-decoration: none;
}

.icp-beian a:hover {
  color: #666;
  text-decoration: underline;
}
</style>