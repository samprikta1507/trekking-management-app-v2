<template>
    <div>
        <h1>Admin Dashboard</h1>

        <button @click="logout">Logout</button>

        <!-- TAB BUTTONS -->
        <div style="margin-bottom: 20px;">
            <button @click="activeTab = 'staff'">Staff</button>
            <button @click="activeTab = 'trek'">Trek</button>
            <button @click="activeTab = 'user'">Users</button>
            <button @click="activeTab = 'history'">Booking History</button>
        </div>

        <!-- SECTIONS -->
        <div v-if="activeTab === 'staff'">
            <StaffManagement />
        </div>

        <div v-if="activeTab === 'trek'">
            <TrekManagement />
        </div>

        <div v-if="activeTab === 'user'">
            <UserManagement />
        </div>

        <div v-if="activeTab === 'history'">
            <BookingHistory />
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import StaffManagement from './StaffManagement.vue'
import TrekManagement from './TrekManagement.vue'
import UserManagement from './UserManagement.vue'
import BookingHistory from './BookingHistory.vue'

export default {
    name: 'AdminDashboard',
    components: {
        StaffManagement,
        TrekManagement,
        UserManagement,
        BookingHistory
    },
    data() {
        return {
            activeTab: 'staff'
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            
            this.$router.push('/login')
        }
    }
}

</script>