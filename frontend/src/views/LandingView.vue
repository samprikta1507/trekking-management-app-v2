<template>
  <div class="container-fluid d-flex flex-column justify-content-center align-items-center text-center" style="min-height: 100vh;">
    
    <div class="mb-5">
      <h1 class="display-3 fw-bold text-info mb-3">Trekking Management</h1>
      <p class="lead text-secondary mx-auto" style="max-width: 600px;">
        Discover breathtaking trails, seamlessly book your next adventure, and manage your journeys all in one place.
      </p>
    </div>

    <div class="d-flex gap-4">
      <button class="btn btn-primary btn-lg px-5 py-3 fw-bold rounded-pill shadow" @click="$router.push('/register')">
        Get Started
      </button>
      <button class="btn btn-outline-light btn-lg px-5 py-3 fw-bold rounded-pill shadow" @click="$router.push('/login')">
        Login
      </button>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'LandingView',
}
</script>