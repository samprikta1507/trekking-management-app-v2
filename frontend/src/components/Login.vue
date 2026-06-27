<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card text-bg-dark border-secondary shadow-lg" style="width: 100%; max-width: 400px;">
      <div class="card-body p-5">
        <div class="text-center mb-4">
            <div class="mb-4">
              <button class="btn btn-sm btn-outline-secondary" @click="$router.push('/')">
                Back to Home
              </button>
            </div>
            <h2 class="fw-bold text-info">Welcome Back</h2>
            <p class="text-secondary small">Please sign in to your account</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label text-light small">Email Address</label>
            <input type="email" class="form-control text-bg-dark border-secondary" v-model="form.email" required>
          </div>
          <div class="mb-4">
            <label class="form-label text-light small">Password</label>
            <input type="password" class="form-control text-bg-dark border-secondary" v-model="form.password" required>
          </div>
          <button type="submit" class="btn btn-primary w-100 py-2 fw-bold shadow-sm">Login</button>
        </form>
        
        <div class="text-center mt-4">
          <span class="text-secondary small">Don't have an account? </span>
          <a href="#" class="text-info text-decoration-none small fw-bold" @click.prevent="$router.push('/register')">Register Here</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Login',

    data() {
        return {
            form: {
                email: '',
                password: ''
            }
        }
    },

    methods: {
        async handleLogin() {
            try {

                const response = await axios.post('http://localhost:5000/api/login', this.form)

                alert(response.data.message)

                localStorage.setItem('token', response.data.token)
                localStorage.setItem('role', response.data.role)
                localStorage.setItem('email', response.data.email)


                const role = response.data.role

                if (role === 'admin') {
                   this.$router.push('/admin')
                }
                
                else if (role === 'staff') {
                   this.$router.push('/staff')
                }
                
                else if (role === 'user') {
                   this.$router.push('/user')
                }

            } catch (error) {

                alert(error.response?.data?.message || 'Login Failed')
                console.error(error)
            }
        }
    }
}
</script>