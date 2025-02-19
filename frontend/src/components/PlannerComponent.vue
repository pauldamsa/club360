<template>
    <div class="flex h-screen flex-col overflow-hidden p-5">
        <Calendar
            :config="{
                defaultMode: 'Week',
                isEditMode: true,
                startTime: '07:00:00',
                endTime: '11:00:00',
                allowCustomClickEvents: true,
                redundantCellHeight: 100,
                enableShortcuts: false,
            }"
            :events="events"
            :create="(event) => logEvent('createEvent', event)"
            :update="(event) => logEvent('updateEvent', event)"
            :delete="(event) => logEvent('deleteEvent', event)"
        />
    </div>
</template>

<script setup>
import { Calendar } from 'frappe-ui';
import { ref } from 'vue';

const events = ref([]);

function logEvent(type, event) {
    console.log(type, event);
}
</script>