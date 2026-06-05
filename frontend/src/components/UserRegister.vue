<template>
    <div>
        <h1>User Registration</h1>
        <form @submit.prevent="handleRegister">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" v-model="form.username" required>
            </div>
            <div>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" v-model="form.email" required>
            </div>
            <div>
                <label for="phone">Phone:</label>
                <input type="text" id="phone" name="phone" v-model="form.phone" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" v-model="form.password" required>
            </div>
            <button type="submit">Register</button>
        </form>

    </div>
    <p>
        Already have an account?
        <a @click="$router.push('/login')">Login</a>
    </p>

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