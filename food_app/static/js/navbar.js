document.write(
    `
    <header class="p-3 mb-3">
    <div class="container">
        <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
            <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 link-body-emphasis text-decoration-none">
                <img src="{{ url_for('static', filename='images/logo.svg') }}" alt="Logo" height="20px">
            </a>

            <ul class="nav col-12 col-lg-auto me-lg-auto ms-2 mb-2 justify-content-center mb-md-0">
                <li><a href="#" class="nav-link px-2 nav-link-style">Home</a></li>
                <li><a href="#" class="nav-link px-2 nav-link-style">Restaurants</a></li>
                <li><a href="#" class="nav-link px-2 nav-link-style">Reviews</a></li>
                <li><a href="#" class="nav-link px-2 nav-link-style">Bookings</a></li>
            </ul>

            <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
                <input type="search" class="form-control" placeholder="Search..." aria-label="Search">
            </form>

            <div class="dropdown text-end">
                <a href="#" class="d-block link-body-emphasis text-decoration-none dropdown-toggle"
                    data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fa-solid fa-circle-user"></i>
                </a>
                <ul class="dropdown-menu text-small">
                    <li><a class="dropdown-item my-dd-item" href="#">Hi, Username</a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item my-dd-item" href="#">My Reviews</a></li>
                    <li><a class="dropdown-item my-dd-item" href="#">My Bookings</a></li>
                    <li><a class="dropdown-item my-dd-item" href="#">My Orders</a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item logout-item" href="#">Logout</a></li>
                </ul>
            </div>
        </div>
    </div>
</header>
`

)