<template>
    <div>
        <h1>Admin Dashboard</h1>

        <!-- TAB BUTTONS -->
        <div style="margin-bottom: 20px;">
            <button @click="activeTab = 'staff'">Staff</button>
            <button @click="activeTab = 'trek'">Trek</button>
            <button @click="activeTab = 'user'">Users</button>
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

    </div>
</template>

<script>
import axios from 'axios'
import StaffManagement from './StaffManagement.vue'
import TrekManagement from './TrekManagement.vue'
import UserManagement from './UserManagement.vue'

export default {
    name: 'AdminDashboard',
    components: {
        StaffManagement,
        TrekManagement,
        UserManagement
    },
    data() {
        return {
            activeTab: 'staff'
        }
    }
}

</script>