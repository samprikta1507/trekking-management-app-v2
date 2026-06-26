<template>
  <div class="container mt-4">
    <h3 class="mb-4">Summary</h3>
    
    <div v-if="loading" class="text-center">
      <p>Loading statistics</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div class="row mb-5">
        <div class="col-md-3">
          <div class="card text-white bg-primary mb-3 text-center">
            <div class="card-body">
              <h5 class="card-title">Total Treks</h5>
              <h2 class="card-text">{{ summaryData.total_treks }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-success mb-3 text-center">
            <div class="card-body">
              <h5 class="card-title">Total Users</h5>
              <h2 class="card-text">{{ summaryData.total_users }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-info mb-3 text-center">
            <div class="card-body">
              <h5 class="card-title">Total Bookings</h5>
              <h2 class="card-text">{{ summaryData.total_bookings }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-warning mb-3 text-center">
            <div class="card-body">
              <h5 class="card-title">Pending Payments</h5>
              <h2 class="card-text">{{ summaryData.pending_payments }}</h2>
            </div>
          </div>
        </div>
      </div>


      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title text-center">Booking Status Breakdown</h5>
              <Pie :data="chartData" :options="chartOptions" />
            </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

const summaryData = ref({})
const loading = ref(true)
const error = ref(null)

const chartData = ref({
  labels: ['Booked', 'Cancelled'],
  datasets: [
    {
      backgroundColor: ['#28a745', '#dc3545'],
      data: [0, 0]
    }
  ]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true
}

const fetchSummary = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/admin/summary', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch summary data')
    }
    
    const data = await response.json()
    summaryData.value = data
    
    chartData.value.datasets[0].data = [
      data.booking_stats.booked,
      data.booking_stats.cancelled
    ]
    
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSummary()
})
</script>