// Opportunity Management System - Frontend JavaScript
// This file handles UI interactions and calls the Python API endpoints

// Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
const HEALTH_URL = 'http://127.0.0.1:8000/health';

// Global state
let currentOpportunities = [];
let currentPage = 1;
let totalPages = 1;
let currentOpportunityId = null;
let skillsCounter = 0;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Opportunity Management System...');
    
    // Check API health
    checkAPIHealth();
    
    // Load dashboard data
    loadDashboard();
    
    // Set up form handlers
    setupFormHandlers();
    
    // Set up search functionality
    setupSearchHandlers();
    
    // Set up character counter for problem statement
    setupProblemStatementCounter();
    
    console.log('Application initialized successfully');
});

// API Health Check
async function checkAPIHealth() {
    try {
        const response = await fetch(HEALTH_URL);
        if (response.ok) {
            console.log('✅ API is healthy');
        } else {
            showToast('Warning', 'API health check failed', 'warning');
        }
    } catch (error) {
        console.error('❌ API health check failed:', error);
        showToast('Error', 'Cannot connect to API server', 'danger');
    }
}

// Navigation Functions
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
        targetSection.classList.add('fade-in');
    }
    
    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Load section-specific data
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'opportunities':
            loadOpportunities();
            break;
        case 'create':
            resetCreateForm();
            break;
    }
}

// Dashboard Functions
async function loadDashboard() {
    try {
        // Call the Python API to get opportunities
        const response = await fetch(`${API_BASE_URL}/opportunities`);
        if (!response.ok) throw new Error('Failed to fetch opportunities');
        
        const data = await response.json();
        const opportunities = data.data.items || [];
        
        updateDashboardStats(opportunities);
        displayRecentOpportunities(opportunities.slice(0, 5));
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Error', 'Failed to load dashboard data', 'danger');
    }
}

function updateDashboardStats(opportunities) {
    const stats = {
        total: opportunities.length,
        draft: opportunities.filter(o => o.status === 'DRAFT').length,
        submitted: opportunities.filter(o => o.status === 'SUBMITTED').length,
        totalRevenue: opportunities.reduce((sum, o) => sum + (o.annual_recurring_revenue || 0), 0)
    };
    
    document.getElementById('total-opportunities').textContent = stats.total;
    document.getElementById('draft-opportunities').textContent = stats.draft;
    document.getElementById('submitted-opportunities').textContent = stats.submitted;
    document.getElementById('total-revenue').textContent = formatCurrency(stats.totalRevenue);
}

function displayRecentOpportunities(opportunities) {
    const container = document.getElementById('recent-opportunities');
    
    if (opportunities.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-briefcase"></i>
                <h5>No Opportunities Yet</h5>
                <p>Create your first opportunity to get started.</p>
                <button class="btn btn-primary" onclick="showSection('create')">
                    <i class="fas fa-plus me-1"></i>Create Opportunity
                </button>
            </div>
        `;
        return;
    }
    
    const tableHTML = `
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Customer</th>
                        <th>Priority</th>
                        <th>Status</th>
                        <th>ARR</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${opportunities.map(opp => `
                        <tr>
                            <td>
                                <strong>${escapeHtml(opp.title)}</strong>
                                <br>
                                <small class="text-muted">${escapeHtml(opp.description.substring(0, 100))}${opp.description.length > 100 ? '...' : ''}</small>
                            </td>
                            <td>${escapeHtml(opp.customer_name)}</td>
                            <td><span class="priority-badge priority-${opp.priority.toLowerCase()}">${opp.priority}</span></td>
                            <td><span class="status-badge status-${opp.status.toLowerCase()}">${opp.status}</span></td>
                            <td>${formatCurrency(opp.annual_recurring_revenue)}</td>
                            <td>${formatDate(opp.created_at)}</td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewOpportunity('${opp.id}')" title="View Details">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    ${opp.status === 'DRAFT' ? `
                                        <button class="btn btn-sm btn-outline-success" onclick="submitOpportunity('${opp.id}')" title="Submit">
                                            <i class="fas fa-paper-plane"></i>
                                        </button>
                                    ` : ''}
                                </div>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

// Opportunities List Functions
async function loadOpportunities(page = 1) {
    try {
        const searchQuery = document.getElementById('search-input')?.value || '';
        const statusFilter = document.getElementById('status-filter')?.value || '';
        const priorityFilter = document.getElementById('priority-filter')?.value || '';
        
        let url = `${API_BASE_URL}/opportunities?page=${page}&page_size=20`;
        if (searchQuery) url += `&query=${encodeURIComponent(searchQuery)}`;
        if (statusFilter) url += `&status=${statusFilter}`;
        if (priorityFilter) url += `&priority=${priorityFilter}`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch opportunities');
        
        const data = await response.json();
        currentOpportunities = data.data.items || [];
        currentPage = data.pagination?.page || 1;
        totalPages = data.pagination?.total_pages || 1;
        
        displayOpportunitiesTable(currentOpportunities);
        
    } catch (error) {
        console.error('Error loading opportunities:', error);
        showToast('Error', 'Failed to load opportunities', 'danger');
    }
}

function displayOpportunitiesTable(opportunities) {
    const container = document.getElementById('opportunities-table');
    
    if (opportunities.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h5>No Opportunities Found</h5>
                <p>Try adjusting your search criteria or create a new opportunity.</p>
            </div>
        `;
        return;
    }
    
    const tableHTML = `
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Customer</th>
                        <th>Priority</th>
                        <th>Status</th>
                        <th>ARR</th>
                        <th>Region</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${opportunities.map(opp => `
                        <tr>
                            <td>
                                <strong>${escapeHtml(opp.title)}</strong>
                                <br>
                                <small class="text-muted">${escapeHtml(opp.description.substring(0, 80))}${opp.description.length > 80 ? '...' : ''}</small>
                            </td>
                            <td>${escapeHtml(opp.customer_name)}</td>
                            <td><span class="priority-badge priority-${opp.priority.toLowerCase()}">${opp.priority}</span></td>
                            <td><span class="status-badge status-${opp.status.toLowerCase()}">${opp.status}</span></td>
                            <td>${formatCurrency(opp.annual_recurring_revenue)}</td>
                            <td>${escapeHtml(opp.geographic_requirements?.name || 'N/A')}</td>
                            <td>${formatDate(opp.created_at)}</td>
                            <td>
                                <div class="action-buttons">
                                    <button class="btn btn-sm btn-outline-primary" onclick="viewOpportunity('${opp.id}')" title="View Details">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    ${opp.status === 'DRAFT' ? `
                                        <button class="btn btn-sm btn-outline-success" onclick="submitOpportunity('${opp.id}')" title="Submit">
                                            <i class="fas fa-paper-plane"></i>
                                        </button>
                                        <button class="btn btn-sm btn-outline-warning" onclick="editOpportunity('${opp.id}')" title="Edit">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                    ` : ''}
                                    ${opp.status !== 'COMPLETED' && opp.status !== 'CANCELLED' ? `
                                        <button class="btn btn-sm btn-outline-danger" onclick="cancelOpportunity('${opp.id}')" title="Cancel">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    ` : ''}
                                    ${opp.status === 'CANCELLED' ? `
                                        <button class="btn btn-sm btn-outline-info" onclick="reactivateOpportunity('${opp.id}')" title="Reactivate">
                                            <i class="fas fa-redo"></i>
                                        </button>
                                    ` : ''}
                                </div>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = tableHTML;
}

// Form Functions
function setupFormHandlers() {
    const form = document.getElementById('create-opportunity-form');
    if (form) {
        form.addEventListener('submit', handleCreateOpportunity);
        
        // Remove default HTML5 validation to handle it manually
        form.setAttribute('novalidate', 'true');
    }
}

function setupProblemStatementCounter() {
    const problemContent = document.getElementById('problem-content');
    if (problemContent) {
        problemContent.addEventListener('input', function() {
            const count = this.value.length;
            document.getElementById('problem-char-count').textContent = count;
            
            if (count < 100) {
                document.getElementById('problem-char-count').className = 'text-danger';
            } else {
                document.getElementById('problem-char-count').className = 'text-success';
            }
        });
    }
}

// Custom form validation
function validateForm() {
    const errors = [];
    
    // Validate Basic Info Tab
    const title = document.getElementById('title').value.trim();
    const customerName = document.getElementById('customer-name').value.trim();
    const priority = document.getElementById('priority').value;
    const annualRevenue = document.getElementById('annual-revenue').value;
    const description = document.getElementById('description').value.trim();
    const regionName = document.getElementById('region-name').value.trim();
    
    if (!title) errors.push({ tab: 'basic-tab', field: 'title', message: 'Title is required' });
    if (!customerName) errors.push({ tab: 'basic-tab', field: 'customer-name', message: 'Customer name is required' });
    if (!priority) errors.push({ tab: 'basic-tab', field: 'priority', message: 'Priority is required' });
    if (!annualRevenue || parseFloat(annualRevenue) < 0) errors.push({ tab: 'basic-tab', field: 'annual-revenue', message: 'Valid annual revenue is required' });
    if (!description) errors.push({ tab: 'basic-tab', field: 'description', message: 'Description is required' });
    if (!regionName) errors.push({ tab: 'basic-tab', field: 'region-name', message: 'Region name is required' });
    
    // Validate Problem Statement Tab
    const problemContent = document.getElementById('problem-content').value.trim();
    if (!problemContent) {
        errors.push({ tab: 'problem-tab', field: 'problem-content', message: 'Problem statement is required' });
    } else if (problemContent.length < 100) {
        errors.push({ tab: 'problem-tab', field: 'problem-content', message: 'Problem statement must be at least 100 characters' });
    }
    
    // Validate Skills Tab
    const skillElements = document.querySelectorAll('.skill-item');
    if (skillElements.length === 0) {
        errors.push({ tab: 'skills-tab', field: 'skills', message: 'At least one skill is required' });
    } else {
        const mustHaveSkills = Array.from(skillElements).filter(skill => 
            skill.querySelector('input[name*="[importance]"]').value === 'MUST_HAVE'
        );
        if (mustHaveSkills.length === 0) {
            errors.push({ tab: 'skills-tab', field: 'skills', message: 'At least one "Must Have" skill is required' });
        }
    }
    
    // Validate Timeline Tab
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    if (!startDate) errors.push({ tab: 'timeline-tab', field: 'start-date', message: 'Start date is required' });
    if (!endDate) errors.push({ tab: 'timeline-tab', field: 'end-date', message: 'End date is required' });
    
    if (startDate && endDate && new Date(startDate) >= new Date(endDate)) {
        errors.push({ tab: 'timeline-tab', field: 'end-date', message: 'End date must be after start date' });
    }
    
    return errors;
}

function showValidationErrors(errors) {
    if (errors.length === 0) return;
    
    // Clear previous error styling
    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    
    // Group errors by tab
    const errorsByTab = {};
    errors.forEach(error => {
        if (!errorsByTab[error.tab]) errorsByTab[error.tab] = [];
        errorsByTab[error.tab].push(error);
    });
    
    // Show first tab with errors
    const firstErrorTab = Object.keys(errorsByTab)[0];
    document.getElementById(firstErrorTab).click();
    
    // Add error styling and show first error message
    const firstError = errors[0];
    const field = document.getElementById(firstError.field);
    if (field) {
        field.classList.add('is-invalid');
        field.focus();
    }
    
    // Show error message
    showToast('Validation Error', firstError.message, 'danger');
    
    // Show summary of all errors
    const errorMessages = errors.map(e => e.message).join('\\n');
    console.log('Validation errors:', errorMessages);
}

// Tab Navigation Functions
function nextTab(tabId) {
    const tab = document.getElementById(tabId);
    if (tab) {
        tab.click();
    }
}

function previousTab(tabId) {
    const tab = document.getElementById(tabId);
    if (tab) {
        tab.click();
    }
}

// Skills Management Functions
function addSkill() {
    const skillName = document.getElementById('skill-name').value.trim();
    const skillType = document.getElementById('skill-type').value;
    const importanceLevel = document.getElementById('importance-level').value;
    const proficiencyLevel = document.getElementById('proficiency-level').value;
    
    if (!skillName) {
        showToast('Error', 'Please enter a skill name', 'danger');
        return;
    }
    
    const skillId = `skill-${skillsCounter++}`;
    const skillHTML = `
        <div class="skill-item border rounded p-3 mb-2" id="${skillId}">
            <div class="row align-items-center">
                <div class="col-md-3">
                    <strong>${escapeHtml(skillName)}</strong>
                    <input type="hidden" name="skills[${skillId}][name]" value="${escapeHtml(skillName)}">
                    <input type="hidden" name="skills[${skillId}][type]" value="${skillType}">
                </div>
                <div class="col-md-2">
                    <span class="badge bg-secondary">${skillType}</span>
                </div>
                <div class="col-md-2">
                    <span class="badge ${importanceLevel === 'MUST_HAVE' ? 'bg-danger' : importanceLevel === 'PREFERRED' ? 'bg-warning' : 'bg-info'}">${importanceLevel.replace('_', ' ')}</span>
                    <input type="hidden" name="skills[${skillId}][importance]" value="${importanceLevel}">
                </div>
                <div class="col-md-3">
                    <span class="badge bg-primary">${proficiencyLevel}</span>
                    <input type="hidden" name="skills[${skillId}][proficiency]" value="${proficiencyLevel}">
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeSkill('${skillId}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('skills-container').insertAdjacentHTML('beforeend', skillHTML);
    
    // Clear form
    document.getElementById('skill-name').value = '';
    document.getElementById('skill-type').value = 'TECHNICAL';
    document.getElementById('importance-level').value = 'MUST_HAVE';
    document.getElementById('proficiency-level').value = 'BEGINNER';
    
    updateSkillsWarning();
}

function removeSkill(skillId) {
    const skillElement = document.getElementById(skillId);
    if (skillElement) {
        skillElement.remove();
        updateSkillsWarning();
    }
}

function updateSkillsWarning() {
    const skills = document.querySelectorAll('.skill-item');
    const mustHaveSkills = Array.from(skills).filter(skill => 
        skill.querySelector('input[name*="[importance]"]').value === 'MUST_HAVE'
    );
    
    const warning = document.getElementById('skills-warning');
    if (mustHaveSkills.length === 0 && skills.length > 0) {
        warning.style.display = 'block';
    } else {
        warning.style.display = 'none';
    }
}

// Create Opportunity Functions
async function handleCreateOpportunity(event) {
    event.preventDefault();
    
    // Custom validation
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
        showValidationErrors(validationErrors);
        return;
    }
    
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Creating...';
    submitButton.disabled = true;
    
    try {
        // Step 1: Create the basic opportunity
        const opportunityData = {
            title: document.getElementById('title').value.trim(),
            customer_id: generateUUID(),
            customer_name: document.getElementById('customer-name').value.trim(),
            sales_manager_id: generateUUID(), // In real app, this would be the logged-in user
            description: document.getElementById('description').value.trim(),
            priority: document.getElementById('priority').value,
            annual_recurring_revenue: parseFloat(document.getElementById('annual-revenue').value),
            geographic_requirements: {
                region_id: generateUUID(),
                name: document.getElementById('region-name').value.trim(),
                requires_physical_presence: document.getElementById('requires-physical').checked,
                allows_remote_work: document.getElementById('allows-remote').checked
            }
        };
        
        const opportunityResponse = await fetch(`${API_BASE_URL}/opportunities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(opportunityData)
        });
        
        if (!opportunityResponse.ok) {
            const errorData = await opportunityResponse.json();
            throw new Error(errorData.error?.message || 'Failed to create opportunity');
        }
        
        const opportunityResult = await opportunityResponse.json();
        const opportunityId = opportunityResult.data.result.id;
        
        // Step 2: Add problem statement
        const problemContent = document.getElementById('problem-content').value.trim();
        if (problemContent) {
            const problemResponse = await fetch(`${API_BASE_URL}/opportunities/${opportunityId}/problem-statement`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: problemContent })
            });
            
            if (!problemResponse.ok) {
                console.warn('Failed to add problem statement, but continuing...');
            }
        }
        
        // Step 3: Add skills
        const skillElements = document.querySelectorAll('.skill-item');
        for (const skillElement of skillElements) {
            const skillName = skillElement.querySelector('input[name*="[name]"]').value;
            const skillData = {
                skill_id: generateUUID(),
                skill_name: skillName, // 添加 skill_name 字段
                skill_type: skillElement.querySelector('input[name*="[type]"]').value,
                importance_level: skillElement.querySelector('input[name*="[importance]"]').value,
                minimum_proficiency_level: skillElement.querySelector('input[name*="[proficiency]"]').value
            };
            
            try {
                await fetch(`${API_BASE_URL}/opportunities/${opportunityId}/skill-requirements`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(skillData)
                });
            } catch (error) {
                console.warn(`Failed to add skill ${skillName}:`, error);
            }
        }
        
        // Step 4: Add timeline
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        if (startDate && endDate) {
            const specificDaysText = document.getElementById('specific-days').value.trim();
            const timelineData = {
                start_date: startDate,
                end_date: endDate,
                is_flexible: document.getElementById('timeline-flexible').checked,
                specific_days: specificDaysText ? specificDaysText.split(',').map(d => d.trim()).filter(d => d) : null
            };
            
            try {
                await fetch(`${API_BASE_URL}/opportunities/${opportunityId}/timeline-requirement`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(timelineData)
                });
            } catch (error) {
                console.warn('Failed to add timeline:', error);
            }
        }
        
        showToast('Success', 'Opportunity created successfully!', 'success');
        
        // Reset form and redirect
        resetCreateForm();
        setTimeout(() => {
            showSection('opportunities');
        }, 1500);
        
    } catch (error) {
        console.error('Error creating opportunity:', error);
        showToast('Error', error.message || 'Failed to create opportunity', 'danger');
    } finally {
        // Restore button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    }
}

async function saveDraft() {
    // Similar to handleCreateOpportunity but without timeline requirement validation
    showToast('Info', 'Draft functionality will be implemented', 'info');
}

function resetCreateForm() {
    const form = document.getElementById('create-opportunity-form');
    if (form) {
        form.reset();
        // Clear skills
        document.getElementById('skills-container').innerHTML = '';
        skillsCounter = 0;
        updateSkillsWarning();
        // Reset to first tab
        document.getElementById('basic-tab').click();
        // Reset character counter
        document.getElementById('problem-char-count').textContent = '0';
        document.getElementById('problem-char-count').className = 'text-muted';
        // Set default values
        document.getElementById('allows-remote').checked = true;
    }
}

// Opportunity Actions
async function viewOpportunity(opportunityId) {
    try {
        const response = await fetch(`${API_BASE_URL}/opportunities/${opportunityId}`);
        if (!response.ok) throw new Error('Failed to fetch opportunity details');
        
        const data = await response.json();
        const details = data.data.result;
        
        displayOpportunityDetails(details);
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('opportunityModal'));
        modal.show();
        
    } catch (error) {
        console.error('Error viewing opportunity:', error);
        showToast('Error', 'Failed to load opportunity details', 'danger');
    }
}

async function submitOpportunity(opportunityId) {
    if (!confirm('Are you sure you want to submit this opportunity? Once submitted, it will be sent for Solution Architect matching.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/opportunities/${opportunityId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: generateUUID() }) // In real app, use actual user ID
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || 'Failed to submit opportunity');
        }
        
        showToast('Success', 'Opportunity submitted successfully!', 'success');
        loadOpportunities(); // Refresh the list
        loadDashboard(); // Refresh dashboard stats
        
    } catch (error) {
        console.error('Error submitting opportunity:', error);
        showToast('Error', error.message || 'Failed to submit opportunity', 'danger');
    }
}

async function cancelOpportunity(opportunityId) {
    const reason = prompt('Please provide a reason for cancelling this opportunity:');
    if (!reason || reason.trim() === '') {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/opportunities/${opportunityId}/cancel`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                user_id: generateUUID(), // In real app, use actual user ID
                reason: reason.trim()
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || 'Failed to cancel opportunity');
        }
        
        showToast('Success', 'Opportunity cancelled successfully!', 'success');
        loadOpportunities(); // Refresh the list
        loadDashboard(); // Refresh dashboard stats
        
    } catch (error) {
        console.error('Error cancelling opportunity:', error);
        showToast('Error', error.message || 'Failed to cancel opportunity', 'danger');
    }
}

async function reactivateOpportunity(opportunityId) {
    if (!confirm('Are you sure you want to reactivate this cancelled opportunity?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/opportunities/${opportunityId}/reactivate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: generateUUID() }) // In real app, use actual user ID
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || 'Failed to reactivate opportunity');
        }
        
        showToast('Success', 'Opportunity reactivated successfully!', 'success');
        loadOpportunities(); // Refresh the list
        loadDashboard(); // Refresh dashboard stats
        
    } catch (error) {
        console.error('Error reactivating opportunity:', error);
        showToast('Error', error.message || 'Failed to reactivate opportunity', 'danger');
    }
}

function displayOpportunityDetails(details) {
    const container = document.getElementById('opportunity-details');
    const opp = details.opportunity;
    
    const detailsHTML = `
        <div class="row">
            <div class="col-md-6">
                <div class="detail-item">
                    <div class="detail-label">Title</div>
                    <div class="detail-value"><strong>${escapeHtml(opp.title)}</strong></div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Customer</div>
                    <div class="detail-value">${escapeHtml(opp.customer_name)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Priority</div>
                    <div class="detail-value">
                        <span class="priority-badge priority-${opp.priority.toLowerCase()}">${opp.priority}</span>
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Status</div>
                    <div class="detail-value">
                        <span class="status-badge status-${opp.status.toLowerCase()}">${opp.status}</span>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="detail-item">
                    <div class="detail-label">Annual Recurring Revenue</div>
                    <div class="detail-value">${formatCurrency(opp.annual_recurring_revenue)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Region</div>
                    <div class="detail-value">${escapeHtml(opp.geographic_requirements?.name || 'N/A')}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Work Requirements</div>
                    <div class="detail-value">
                        ${opp.geographic_requirements?.requires_physical_presence ? 
                            '<i class="fas fa-check text-success"></i> Physical Presence Required<br>' : 
                            '<i class="fas fa-times text-muted"></i> Physical Presence Not Required<br>'
                        }
                        ${opp.geographic_requirements?.allows_remote_work ? 
                            '<i class="fas fa-check text-success"></i> Remote Work Allowed' : 
                            '<i class="fas fa-times text-muted"></i> Remote Work Not Allowed'
                        }
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Created</div>
                    <div class="detail-value">${formatDate(opp.created_at)}</div>
                </div>
            </div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">Description</div>
            <div class="detail-value">${escapeHtml(opp.description)}</div>
        </div>
        
        ${details.problem_statement ? `
            <div class="detail-item">
                <div class="detail-label">Problem Statement</div>
                <div class="detail-value">${escapeHtml(details.problem_statement.content)}</div>
            </div>
        ` : ''}
        
        ${details.skill_requirements && details.skill_requirements.length > 0 ? `
            <div class="detail-item">
                <div class="detail-label">Required Skills</div>
                <div class="detail-value">
                    <div class="row">
                        ${details.skill_requirements.map(skill => `
                            <div class="col-md-6 mb-2">
                                <div class="border rounded p-2">
                                    <strong>${escapeHtml(skill.skill_name)}</strong>
                                    <br>
                                    <small>
                                        <span class="badge bg-secondary me-1">${skill.skill_type}</span>
                                        <span class="badge ${skill.importance_level === 'MUST_HAVE' ? 'bg-danger' : skill.importance_level === 'PREFERRED' ? 'bg-warning' : 'bg-info'} me-1">${skill.importance_level.replace('_', ' ')}</span>
                                        <span class="badge bg-primary">${skill.minimum_proficiency_level}</span>
                                    </small>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        ` : ''}
        
        ${details.timeline ? `
            <div class="detail-item">
                <div class="detail-label">Timeline Requirements</div>
                <div class="detail-value">
                    <strong>Start Date:</strong> ${details.timeline.start_date}<br>
                    <strong>End Date:</strong> ${details.timeline.end_date}<br>
                    <strong>Flexible:</strong> ${details.timeline.is_flexible ? 'Yes' : 'No'}
                    ${details.timeline.specific_days ? `<br><strong>Specific Days:</strong> ${details.timeline.specific_days.join(', ')}` : ''}
                </div>
            </div>
        ` : ''}
        
        ${details.status_history && details.status_history.length > 0 ? `
            <div class="detail-item">
                <div class="detail-label">Status History</div>
                <div class="detail-value">
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Status</th>
                                    <th>Reason</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${details.status_history.map(status => `
                                    <tr>
                                        <td><span class="status-badge status-${status.status.toLowerCase()}">${status.status}</span></td>
                                        <td>${escapeHtml(status.reason)}</td>
                                        <td>${formatDate(status.changed_at)}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        ` : ''}
    `;
    
    container.innerHTML = detailsHTML;
    
    // Update modal actions based on opportunity status
    updateOpportunityActions(opp);
}

function updateOpportunityActions(opportunity) {
    const actionsContainer = document.getElementById('opportunity-actions');
    let actionsHTML = '';
    
    if (opportunity.status === 'DRAFT') {
        actionsHTML += `
            <button type="button" class="btn btn-success me-2" onclick="submitOpportunity('${opportunity.id}')">
                <i class="fas fa-paper-plane me-1"></i>Submit
            </button>
            <button type="button" class="btn btn-warning me-2" onclick="editOpportunity('${opportunity.id}')">
                <i class="fas fa-edit me-1"></i>Edit
            </button>
        `;
    }
    
    if (opportunity.status !== 'COMPLETED' && opportunity.status !== 'CANCELLED') {
        actionsHTML += `
            <button type="button" class="btn btn-danger me-2" onclick="cancelOpportunity('${opportunity.id}')">
                <i class="fas fa-times me-1"></i>Cancel
            </button>
        `;
    }
    
    if (opportunity.status === 'CANCELLED') {
        actionsHTML += `
            <button type="button" class="btn btn-info me-2" onclick="reactivateOpportunity('${opportunity.id}')">
                <i class="fas fa-redo me-1"></i>Reactivate
            </button>
        `;
    }
    
    actionsContainer.innerHTML = actionsHTML;
}

// Utility Functions
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount || 0);
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showToast(title, message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    
    // Set content
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    // Set type styling
    toast.className = `toast show bg-${type === 'danger' ? 'danger' : type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'info'} text-white`;
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });
    bsToast.show();
}
