<template>
  <div>
    <h1>Trekking Management App</h1>

    <div @click="$router.push('/register')">
      Register
    </div>

    <div @click="$router.push('/login')">
      Login
    </div>

  </div>
</template>

<script>
export default {
  name: 'LandingView',
}
</script>