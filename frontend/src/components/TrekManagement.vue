<template>
        <h2>Trek Management</h2>

        <button @click="showTrekForm = !showTrekForm">Add Trek</button>
        <div v-if="showTrekForm">

            <h3>Create Trek</h3>

            <form @submit.prevent="saveTrek">

                <div>
                    <label>Trek Name:</label>
                    <input type="text" v-model="trekForm.trek_name">
                </div>

                <div>
                    <label>Location:</label>
                    <input type="text" v-model="trekForm.location">
                </div>

                <div>
                    <label>Difficulty:</label>
                    <input type="text" v-model="trekForm.difficulty">
                </div>

                <div>
                    <label>Duration Days:</label>
                    <input type="number" v-model="trekForm.duration_days">
                </div>

                <div>
                    <label>Available Slots:</label>
                    <input type="number" v-model="trekForm.available_slots">
                </div>

                <div>
                    <label>Assigned Staff ID:</label>
                    <input type="number" v-model="trekForm.assigned_staff_id">
                </div>

                <div>
                    <label>Start Date:</label>
                    <input type="date" v-model="trekForm.start_date">
                </div>

                <div>
                    <label>End Date:</label>
                    <input type="date" v-model="trekForm.end_date">
                </div>

                <div>
                    <label>Price:</label>
                    <input type="number" v-model="trekForm.price">
                </div>

                <button type="submit">{{ isEditingTrek ? 'Update Trek' : 'Create Trek' }}</button>

            </form>

        </div>

        <h3>Trek List</h3>

        <div v-for="trek in trekList" :key="trek.id">
        
            <p>Trek Name: {{ trek.trek_name }}</p>
        
            <p>Location: {{ trek.location }}</p>
        
            <p>Difficulty: {{ trek.difficulty }}</p>
        
            <p>Duration: {{ trek.duration_days }} days</p>
        
            <p>Available Slots: {{ trek.available_slots }}</p>
        
            <p>Status: {{ trek.status }}</p>
        
            <p>Price: ₹{{ trek.price }}</p>

            <button @click="editTrek(trek)">Edit</button>
            <button @click="deleteTrek(trek.id)">Delete</button>
        
            <hr>
        
        </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'TrekManagement',

    data() {
        return {
            trekList: [],

            showTrekForm: false,
                    
            isEditingTrek: false,
                    
            editingTrekId: null,
                    
            trekForm: {
                trek_name: '',
                location: '',
                difficulty: '',
                duration_days: '',
                available_slots: '',
                assigned_staff_id: '',
                start_date: '',
                end_date: '',
                price: '',
                status: 'Pending'
            },
        }
    },

    async mounted() {
        try {
            const token = localStorage.getItem('token')
        
            const trekResponse = await axios.get(
                'http://localhost:5000/api/admin/treks',
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )
            
            this.trekList = trekResponse.data
            
        } catch (error) {
            console.error(error)
        }
    },

    methods: {
                async createTrek() {

            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.post(
                    'http://localhost:5000/api/admin/create-trek',
                    this.trekForm,
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
                    'Failed to create trek'
                )
            
            }
        
        },

        async saveTrek() {

            if (this.isEditingTrek) {
            
                this.updateTrek()
            
            } else {
            
                this.createTrek()
            
            }
        
        },

        async deleteTrek(trekId) {

            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.delete(
                    `http://localhost:5000/api/admin/delete-trek/${trekId}`,
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
                    'Failed to delete trek'
                )
            
            }
        
        },

        async updateTrek() {
                
            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.put(
                    `http://localhost:5000/api/admin/update-trek/${this.editingTrekId}`,
                    this.trekForm,
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
                    'Failed to update trek'
                )
            
            }
        
        },

        editTrek(trek) {

            this.showTrekForm = true

            this.isEditingTrek = true

            this.editingTrekId = trek.id

            this.trekForm.trek_name = trek.trek_name
            this.trekForm.location = trek.location
            this.trekForm.difficulty = trek.difficulty
            this.trekForm.duration_days = trek.duration_days
            this.trekForm.available_slots = trek.available_slots
            this.trekForm.assigned_staff_id = trek.assigned_staff_id
            this.trekForm.start_date = trek.start_date
            this.trekForm.end_date = trek.end_date
            this.trekForm.price = trek.price
            this.trekForm.status = trek.status

        },
    }
}
</script>