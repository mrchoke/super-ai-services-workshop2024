<script setup>
  import { useFetch } from '@vueuse/core'
  import { ref } from 'vue'

  const input = ref('')
  const qr = ref(null)

  const generateQR = () => {
    if (input.value) {
      const { data, onFetchFinally } = useFetch(`/api/qrcode?text=${input.value}`).blob()
      onFetchFinally(() => {
        qr.value = URL.createObjectURL(data.value)
      })
    }
  }

  const downloadQR = () => {
    const a = document.createElement('a')
    a.href = qr.value
    a.download = 'qrcode.png'
    a.click()
  }
</script>

<template>
  <div class="flex flex-col px-3">
    <h1 class="text-4xl font-bold text-center my-5">Quick QR</h1>
    <input type="text" v-model="input" class="border-2 border-gray-300 p-2 rounded-lg w-full"
      placeholder="Enter text to generate QR code" />
    <button class="w-1/2 bg-blue-500 text-white p-2 rounded-lg mx-auto my-4" @click="generateQR">Generate QR</button>
    <img v-if="qr" :src="qr" alt="QR Code" class="mx-auto mt-5 w-1/2" />
    <button v-if="qr" class="w-1/2 bg-blue-500 text-white p-2 rounded-lg mx-auto my-4" @click="downloadQR">Download
      QR</button>
  </div>

</template>
