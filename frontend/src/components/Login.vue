<template>
    <div>
        <h1>Login</h1>

        <form @submit.prevent="handleLogin">

            <div>
                <label>Email:</label>
                <input type="email" v-model="form.email" required>
            </div>

            <div>
                <label>Password:</label>
                <input type="password" v-model="form.password" required>
            </div>

            <button type="submit">Login</button>

        </form>
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