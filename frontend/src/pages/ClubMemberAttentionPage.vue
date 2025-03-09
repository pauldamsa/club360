<template>
    <div class="p-4 md:p-6 space-y-4 md:space-y-6">
        <!-- Loading indicator -->
        <div v-if="isLoading" class="flex justify-center items-center py-8">
            <div class="flex items-center space-x-2">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                <span class="text-gray-500">Loading members data...</span>
            </div>
        </div>
        
        <!-- Rest of existing template with v-else -->
        <div v-else>
            <!-- Header -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between space-y-3 sm:space-y-0">
                <div>
                    <h1 class="text-xl md:text-2xl font-bold text-gray-900">To Be Inactive Members</h1>
                    <p class="mt-1 text-sm text-gray-500">Members with expiring memberships or low visits</p>
                </div>
                <Badge 
                    :label="attentionMembers.length"
                    class="text-sm md:text-base bg-red-100 text-red-800 self-start sm:self-center"
                />
            </div>

            <!-- Members List -->
            <div class="space-y-4">
                <div v-if="!attentionMembers.length" class="text-center py-8 text-gray-500">
                    No members need attention at this time.
                </div>
                
                <!-- Mobile View -->
                <div class="block sm:hidden space-y-4">
                    <Card v-for="member in attentionMembers" 
                        :key="member.name" 
                        class="bg-white"
                    >
                        <div class="p-4 space-y-4">
                            <!-- Member Info -->
                            <div class="flex items-start justify-between">
                                <div class="flex items-center space-x-3">
                                    <Avatar :label="member.full_name" size="md" />
                                    <div>
                                        <h3 class="font-medium text-gray-900">{{ member.full_name }}</h3>
                                        <p class="text-sm text-gray-500">Coach: {{ getCoachName(member.coach) }}</p>
                                    </div>
                                </div>
                                <Button
                                    variant="outline"
                                    icon="edit-2"
                                    size="sm"
                                    @click="editMember(member)"
                                />
                            </div>

                            <!-- Membership Status -->
                            <div class="space-y-2">
                                <div v-for="(membership, index) in member.memberships" 
                                    :key="index"
                                    class="p-3 bg-gray-50 rounded-lg space-y-2"
                                >
                                    <div class="flex justify-between text-sm">
                                        <span class="text-gray-600">{{ membership.type }}</span>
                                        <Badge 
                                            :label="membership.remaining_visits + ' visits'"
                                            :class="{
                                                'bg-red-100 text-red-800': membership.remaining_visits <= 3,
                                                'bg-yellow-100 text-yellow-800': membership.remaining_visits > 3
                                            }"
                                        />
                                    </div>
                                    <div class="flex justify-between text-sm">
                                        <span class="text-gray-600">Expires</span>
                                        <span :class="{
                                            'text-red-600': isExpiringSoon(membership.end_date),
                                            'text-gray-600': !isExpiringSoon(membership.end_date)
                                        }">
                                            {{ formatDate(membership.end_date) }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Card>
                </div>

                <!-- Desktop View -->
                <div class="hidden sm:block">
                    <Card>
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Member</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Coach</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Membership</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expires</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Visits Left</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="member in attentionMembers" :key="member.name">
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center space-x-3">
                                            <Avatar :label="member.full_name" size="sm" />
                                            <div class="font-medium text-gray-900">{{ member.full_name }}</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        {{ getCoachName(member.coach) }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        {{ member.memberships[0]?.type }}
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span :class="{
                                            'text-red-600': isExpiringSoon(member.memberships[0]?.end_date),
                                            'text-gray-600': !isExpiringSoon(member.memberships[0]?.end_date)
                                        }">
                                            {{ formatDate(member.memberships[0]?.end_date) }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <Badge 
                                            :label="member.memberships[0]?.remaining_visits"
                                            :class="{
                                                'bg-red-100 text-red-800': member.memberships[0]?.remaining_visits <= 3,
                                                'bg-yellow-100 text-yellow-800': member.memberships[0]?.remaining_visits > 3
                                            }"
                                        />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <Button
                                            variant="outline"
                                            icon="edit-2"
                                            size="sm"
                                            @click="editMember(member)"
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </Card>
                </div>
            </div>
        </div>
    </div>

    <EditMemberDialog ref="editMemberDialog" />
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { Card, Badge, Avatar, Button, createListResource, createDocumentResource } from 'frappe-ui';
import { addDays, parseISO, isPast, isWithinInterval } from 'date-fns';
import EditMemberDialog from '@/components/EditMemberDialog.vue';
import { session } from '@/data/session';
import { useRoute } from 'vue-router';

// Loading state and refs
const isLoading = ref(true);
const editMemberDialog = ref(null);
const loadingTimeout = ref(null);
const route = useRoute();
const memberDetails = ref(new Map()); // Store detailed member data

// Step 1: Get basic list of active members first
const membersResource = createListResource({
    doctype: 'Club Member',
    fields: ['name', 'full_name', 'coach'],
    filters: {
        owner: session.user,
        status: 'Active'
    },
    auto: true, // Auto-fetch the basic list
    onSuccess: (data) => {
        if (data && data.length > 0) {
            // Track progress for detailed fetches
            let fetchedCount = 0;
            const totalMembers = data.length;
            
            // Set a timeout in case fetches take too long
            // startLoadingTimeout();
            
            // Fetch detailed data for each member
            data.forEach(member => {
                fetchMemberDetails(member.name, () => {
                    fetchedCount++;
                    // When all members are fetched, we're done loading
                    if (fetchedCount >= totalMembers) {
                        isLoading.value = false;
                        clearLoadingTimeout();
                    }
                });
            });
        } else {
            isLoading.value = false; // No members to load
        }
    },
    onError: () => {
        isLoading.value = false; // Error occurred, stop loading
    }
});

// Step 2: Function to fetch detailed data for each member
function fetchMemberDetails(memberId, callback) {
    createDocumentResource({
        doctype: 'Club Member',
        name: memberId,
        fields: ['*'], // Get all fields including child tables
        auto: true,
        onSuccess: (data) => {
            // Store the detailed member data
            memberDetails.value.set(memberId, data);
            // Force reactivity update
            memberDetails.value = new Map(memberDetails.value);
            if (callback) callback();
        },
        onError: (error) => {
            console.error(`Error fetching details for member ${memberId}:`, error);
            if (callback) callback(); // Still call callback to continue progress
        }
    });
}

// Step 3: Safety timeout to prevent eternal loading
function startLoadingTimeout() {
    if (loadingTimeout.value) clearTimeout(loadingTimeout.value);
    loadingTimeout.value = setTimeout(() => {
        if (isLoading.value) {
            console.warn('Loading timeout reached');
            isLoading.value = false;
        }
    }, 10000); // 10 seconds timeout
}

function clearLoadingTimeout() {
    if (loadingTimeout.value) {
        clearTimeout(loadingTimeout.value);
        loadingTimeout.value = null;
    }
}

// Get coaches for name mapping
const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['id_herbalife', 'full_name'],
    filters: {
        owner: session.user
    },
    auto: true
});

// Step 4: Updated attentionMembers computed that uses memberDetails
const attentionMembers = computed(() => {
    if (!membersResource.list.data || memberDetails.value.size === 0) return [];
    
    return membersResource.list.data
        .filter(member => {
            // Get detailed member info from our map
            const details = memberDetails.value.get(member.name);
            if (!details?.memberships?.length) return false;
            
            // Get the latest membership
            const latestMembership = details.memberships[details.memberships.length - 1];
            if (!latestMembership) return false;
            
            try {
                // Check if the member needs attention
                const endDate = parseISO(latestMembership.end_date);
                const today = new Date();
                const fourDaysFromNow = addDays(today, 4);
                
                return (
                    latestMembership.remaining_visits <= 3 || // Low visits
                    isPast(endDate) || // Already expired
                    isWithinInterval(endDate, { start: today, end: fourDaysFromNow }) // Expiring soon
                );
            } catch (error) {
                console.error('Error processing member data:', error);
                return false;
            }
        })
        .map(member => {
            // Combine basic member data with detailed data including memberships
            return {
                ...member,
                ...memberDetails.value.get(member.name)
            };
        });
});

// Step 5: Cleanup on component unmount
onMounted(() => {
    startLoadingTimeout();
});

onBeforeUnmount(() => {
    clearLoadingTimeout();
});

// Step 6: Function to manually reload all data
function reloadData() {
    isLoading.value = true;
    memberDetails.value.clear();
    startLoadingTimeout();
    membersResource.reload();
}

// Helper functions
function getCoachName(coachId) {
    if (!coachesResource.list.data) return 'Loading...';
    const coach = coachesResource.list.data.find(c => c.id_herbalife === coachId);
    return coach?.full_name || 'No Coach';
}

function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString();
}

function isExpiringSoon(dateString) {
    if (!dateString) return false;
    try {
        const endDate = parseISO(dateString);
        const fourDaysFromNow = addDays(new Date(), 4);
        return isWithinInterval(endDate, { start: new Date(), end: fourDaysFromNow });
    } catch (error) {
        console.error('Error checking if date is expiring soon:', error);
        return false;
    }
}

function editMember(member) {
    editMemberDialog.value?.openDialog(member);
}

defineExpose({ reloadData });
</script>