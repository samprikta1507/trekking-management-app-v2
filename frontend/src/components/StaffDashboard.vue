<template>
    <div>

        <h1>Staff Dashboard</h1>

        <h2>My Assigned Treks</h2>

        <div v-for="trek in treks" :key="trek.id">
            <hr>

            <p><strong>Name:</strong> {{ trek.trek_name }}</p>

            <p><strong>Location:</strong> {{ trek.location }}</p>

            <p><strong>Difficulty:</strong> {{ trek.difficulty }}</p>

            <p><strong>Available Slots:</strong> {{ trek.available_slots }}</p>

            <p><strong>Status:</strong> {{ trek.status }}</p>

            <p><strong>Registered Trekkers:</strong> {{ trek.registered_trekkers }}</p>

            <h4>Update Slots</h4>

            <input type="number" v-model="trek.available_slots"/>

            <button @click="updateSlots(trek)">Update Slots</button>

            <h4>Update Status</h4>

            <select v-model="trek.status">
            
                <option>Open</option>
            
                <option>Closed</option>
            
                <option>Started</option>
            
                <option>Ongoing</option>
            
                <option>Completed</option>
            
            </select>

            <button @click="updateStatus(trek)">Update Status</button>

        </div>

    </div>
</template>

<script>
import axios from "axios"

export default {

    name: "StaffDashboard",

    data() {
        return {
            treks: []
        }
    },

    async mounted() {

        try {

            const token = localStorage.getItem("token")

            const response = await axios.get(
                "http://127.0.0.1:5000/api/staff/my-treks",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            this.treks = response.data

        }
        catch (error) {

            console.error(error)

        }

    },

    methods: {

        async updateSlots(trek) {
        
            try {
            
                const token = localStorage.getItem("token")
            
                await axios.put(
                    `http://127.0.0.1:5000/api/staff/update-slots/${trek.id}`,
                    {
                        available_slots: trek.available_slots
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                  
                alert("Slots updated successfully")
                  
            }
            catch (error) {
            
                console.error(error)
            
            }
          
        },
      
        async updateStatus(trek) {
        
            try {
            
                const token = localStorage.getItem("token")
            
                await axios.put(
                    `http://127.0.0.1:5000/api/staff/update-status/${trek.id}`,
                    {
                        status: trek.status
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                  
                alert("Status updated successfully")
                  
            }
            catch (error) {
            
                console.error(error)
            
            }
          
        },
      
    }

}
</script>