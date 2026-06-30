<template>
    <div class="admin-page">
        <div class="container-fluid px-5 py-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h1>Admin Dashboard</h1>
              <button class="btn btn-outline-danger" @click="logout">Logout</button>
            </div>

            <!-- TAB BUTTONS -->
            <div style="margin-bottom: 20px;">
                <button class="btn btn-outline-primary" @click="activeTab = 'staff'">Staff</button>
                <button class="btn btn-outline-primary" @click="activeTab = 'trek'">Trek</button>
                <button class="btn btn-outline-primary" @click="activeTab = 'user'">Users</button>
                <button class="btn btn-outline-primary" @click="activeTab = 'history'">Booking History</button>
                <button class="btn btn-outline-primary" @click="activeTab = 'summary'">Summary</button>
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

            <div v-if="activeTab === 'summary'">
              <AdminSummary />
            </div>

        </div>
    </div>
    
</template>

<script>
import axios from 'axios'
import StaffManagement from './StaffManagement.vue'
import TrekManagement from './TrekManagement.vue'
import UserManagement from './UserManagement.vue'
import BookingHistory from './BookingHistory.vue'
import AdminSummary from './AdminSummary.vue'

export default {
    name: 'AdminDashboard',
    components: {
        StaffManagement,
        TrekManagement,
        UserManagement,
        BookingHistory,
        AdminSummary
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