<template>
  <div class="container mt-4">
    <h2 class="mb-4 border-bottom border-secondary pb-2">Platform Booking History</h2>
    
    <div class="table-responsive">
      <table class="table table-dark table-striped table-hover align-middle border-secondary">
        <thead>
          <tr>
            <th>User Name</th>
            <th>Email</th>
            <th>Trek Booked</th>
            <th>Booking Date</th>
            <th>Status</th>
            <th>Payment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookingList" :key="booking.booking_id">
            <td class="fw-bold">{{ booking.user_name }}</td>
            <td>{{ booking.user_email }}</td>
            <td class="text-info">{{ booking.trek_name }}</td>
            <td>{{ booking.booking_date.split(' ')[0] }}</td>
            <td>
              <span class="badge" :class=" booking.status === 'Booked' ? 'bg-success' : booking.status === 'Cancelled' ? 'bg-danger' : booking.status === 'Completed' ? 'bg-primary' : 'bg-warning text-dark'">
                {{ booking.status }}
              </span>
            </td>
            <td>
              <span class="badge" :class="booking.payment_status === 'Paid' ? 'bg-success' : 'bg-warning text-dark'">
                {{ booking.payment_status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
  </div>
</template>

<script>
import axios from "axios"

export default {

    name: "BookingHistory",

    data() {
        return {
            bookingList: []
        }
    },

    async mounted() {

        try {

            const token =
                localStorage.getItem("token")

            const response =
                await axios.get(
                    "http://localhost:5000/api/admin/bookings",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.bookingList = response.data

        }

        catch(error) {

            console.error(error)

        }

    }

}
</script>