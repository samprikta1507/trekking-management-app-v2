<template>
  <div class="container d-flex justify-content-center align-items-center min-vh-100 py-5">
    <div class="card text-bg-dark border-secondary shadow-lg" style="width: 100%; max-width: 500px;">
      <div class="card-body p-5">
        <div class="text-center mb-4">
            <div class="mb-4">
              <button class="btn btn-sm btn-outline-secondary" @click="$router.push('/')">
                Back to Home
              </button>
            </div>
            <h2 class="fw-bold text-info">Create Account</h2>
            <p class="text-secondary small">Join us for your next adventure</p>
        </div>
        
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label class="form-label text-light small">Full Name</label>
            <input type="text" class="form-control text-bg-dark border-secondary" v-model="form.username" required>
          </div>
          <div class="mb-3">
            <label class="form-label text-light small">Email Address</label>
            <input type="email" class="form-control text-bg-dark border-secondary" v-model="form.email" required>
          </div>
          <div class="mb-3">
            <label class="form-label text-light small">Phone Number</label>
            <input type="text" class="form-control text-bg-dark border-secondary" v-model="form.phone" required>
          </div>
          <div class="mb-4">
            <label class="form-label text-light small">Password</label>
            <input type="password" class="form-control text-bg-dark border-secondary" v-model="form.password" minlength="8" required>
          </div>
          <button type="submit" class="btn btn-success w-100 py-2 fw-bold shadow-sm">Register</button>
        </form>
        
        <div class="text-center mt-4">
          <span class="text-secondary small">Already have an account? </span>
          <a href="#" class="text-info text-decoration-none small fw-bold" @click.prevent="$router.push('/login')">Login Here</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'UserRegister',
    emits: ['register-success'],
    data() {
        return {
            form: {
                username: '',
                email: '',
                phone: '',
                password: ''
            }
        }
    },
    methods: {
        async handleRegister() {
            try {
                const response = await axios.post('http://localhost:5000/api/register', this.form)

                alert(response.data.message)

                this.form.username = ''
                this.form.email = ''
                this.form.phone = ''
                this.form.password = ''

                this.$emit('register-success')

            } catch (error) {
                console.error(error)
            }   
        }
    }
}
</script>