<template>
        <h2>User List</h2>

        <div v-for="user in userList" :key="user.id">
        
            <p>Name: {{ user.name }}</p>
        
            <p>Email: {{ user.email }}</p>
        
            <p>Blacklisted: {{ user.is_blacklisted }}</p>

            <button @click="toggleBlacklist(user.id)">{{ user.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}</button>
        
            <hr>
        
        </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'UserManagement',

    data() {
        return {
            userList: []
        }
    },

    async mounted() {
            try {
                const token = localStorage.getItem('token')
            
                const userResponse = await axios.get(
                    'http://localhost:5000/api/admin/users',
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                
                this.userList = userResponse.data
                
            } catch (error) {
                console.error(error)
            }
        },

    methods: {
                async toggleBlacklist(userId) {

            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.put(
                    `http://localhost:5000/api/admin/toggle-blacklist/${userId}`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                
                alert(response.data.message)
                
                window.location.reload()
                
            } catch (error) {
            
                alert(
                    error.response?.data?.message ||
                    'Failed to update blacklist status'
                )
            
            }
        }
    }
}
</script>