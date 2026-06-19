# Dokumentasi Teknis & Skema Arsitektur OOP: Global Scholar Platform

Dokumen ini disusun sebagai panduan cetak biru (*blueprint*) arsitektur perangkat lunak untuk platform **Global Scholar: International Exchange Housing & Buddy Finder**. Panduan ini merinci fungsionalitas sistem, alur proses kerja (*workflow*), serta implementasi tiga pilar utama *Object-Oriented Programming* (OOP) untuk memastikan sistem berjalan dengan modular, aman, dan mudah dikembangkan (*scalable*).

---

## 1. Dekonstruksi Projek: Apa yang Sebenarnya Sedang Digarap?

**Global Scholar** adalah platform ekosistem digital *one-stop solution* yang dirancang khusus untuk mahasiswa yang berpartisipasi dalam program pertukaran pelajar internasional (*international exchange*), seperti ke negara tujuan Korea Selatan, Jepang, atau negara lainnya. 

Tujuan utama dari platform ini adalah memitigasi kendala adaptasi kultural, logistik, dan sosial mahasiswa asing di lingkungan kampus baru melalui tiga pilar fitur:
1. **Buddy Finder (Sistem Pencocokan Pintar):** Menghubungkan mahasiswa pendatang dengan mahasiswa lokal (*local buddy*) atau sesama mahasiswa *exchange* berdasarkan kecocokan gaya hidup dan kebiasaan belajar.
2. **Secure Group Messaging:** Menyediakan ruang komunikasi terenkapsulasi untuk memfasilitasi koordinasi pencarian tempat tinggal komunal secara mandiri.
3. **Student Marketplace (Peer-to-Peer):** Forum terverifikasi khusus mahasiswa untuk melakukan oper kontrak (*subletting*) apartemen/kamar atau jual beli perlengkapan kuliah (seperti buku teks) guna menghemat biaya.

---

## 2. Alur Proses Sistem (System Workflow) Agar Berjalan Sempurna

Agar website dapat berjalan dengan lancar tanpa ada *bug* logika atau kebocoran data, sistem dibagi menjadi 4 fase proses terintegrasi:

| Fase Proses | Mekanisme Kerja Belakang Layar (Backend Engine) | Output Sistem |
| :--- | :--- | :--- |
| **1. Registrasi & Verifikasi** | Mahasiswa mendaftar menggunakan email kampus. Sistem memvalidasi domain email untuk memastikan pengguna adalah mahasiswa asli (*Verified Student*). Atribut sensitif seperti *password* langsung dienkapsulasi. | Akun aktif dengan status `isVerified = true`. |
| **2. Profiling & Matching** | Pengguna mengisi preferensi (jadwal tidur, tingkat kebersihan, preferensi studi). Sistem mengolah data ini ke dalam objek profil terpisah yang terikat mati dengan akun pengguna. Algoritma menghitung matriks kedekatan nilai (*matching score*). | Daftar rekomendasi *roommate* atau *buddy* yang kompatibel. |
| **3. Komunikasi Komunal** | Pengguna yang saling cocok (*matched*) dapat menginisiasi pembuatan grup obrolan untuk mendiskusikan rencana sewa hunian luar kampus (*off-campus housing*). | Terbentuknya ruang *chat group* dinamis yang menampung pesan terenkripsi. |
| **4. P2P Marketplace** | Mahasiswa yang ingin mengoper kamar atau menjual buku membuat unggahan. Sistem membedakan tipe data hunian dan tipe data barang biasa lewat pewarisan objek agar pencarian di web menjadi presisi. | *Feed* katalog interaktif yang terorganisir berdasarkan kategori produk. |

---

## 3. Skema Pemetaan 3 Pilar OOP ke dalam Fitur Sistem

Untuk memenuhi standarisasi arsitektur perangkat lunak yang bersih (*clean code*), project ini mengadopsi tiga prinsip utama OOP:

### A. Inheritance (Pewarisan)
Prinsip ini digunakan untuk mengeliminasi duplikasi kode pada fitur **Marketplace**. Kamar apartemen (`HousingListing`) dan buku teks (`ItemListing`) sama-sama merupakan sebuah iklan produk, namun memiliki detail spesifik yang berbeda.

* **Base Class (Superclass):** `Listing`
    * Menampung atribut umum yang dimiliki semua iklan: `listingID`, `title`, `description`, `datePosted`, dan `owner`.
* **Subclass (Child Class 1):** `HousingListing`
    * Mewarisi seluruh atribut `Listing`, ditambah properti spesifik hunian: `rentPrice`, `address`, `roomCount`, dan `durationMonths`.
* **Subclass (Child Class 2):** `ItemListing`
    * Mewarisi seluruh atribut `Listing`, ditambah properti spesifik barang: `itemPrice`, `itemCondition` (misal: *New, Like New, Used*), dan `category`.

### B. Composition (Komposisi / Hubungan Kepemilikan Kuat)
Prinsip di mana sebuah objek menjadi bagian utuh dari objek lain (*has-a relationship*). Jika objek utama dihancurkan, maka objek di dalamnya ikut musnah.

1.  **Hubungan `User` dan `MatchProfile`:**
    * Objek `User` memiliki secara langsung (*directly owns*) objek `MatchProfile`.
    * Satu profil pencocokan tidak dapat berdiri sendiri di database tanpa adanya akun induk (`User`). Jika seorang mahasiswa menghapus akun `User` mereka, maka objek `MatchProfile` otomatis terhapus secara permanen.
2.  **Hubungan `Group` dan `Message`:**
    * Objek `Group` menampung kumpulan objek `Message` dalam bentuk *list/array*.
    * Jika sebuah grup diskusi hunian dibubarkan atau dihapus oleh admin, seluruh riwayat obrolan (`Message`) di dalamnya ikut dihancurkan dari memori sistem.

### C. Encapsulation (Enkapsulasi & Pembatasan Akses)
Prinsip menyembunyikan data internal objek dan membatasi akses langsung dari luar menggunakan *access modifier* (`private`), serta menyediakannya hanya lewat metode perantara (*getter* dan *setter*).

* **Penerapan Keamanan Data Akun:** Atribut seperti `password`, `email`, dan `isVerified` pada class `User` di-set sebagai `private`. Mengubah status verifikasi hanya bisa dilakukan via method internal sistem setelah lolos validasi dokumen.
* **Penerapan Logika Algoritma:** Atribut `matchScore` di dalam `MatchProfile` bersifat `private`. Komponen luar atau halaman web lain tidak boleh mengubah skor ini secara acak; skor hanya bisa dihitung ulang secara internal oleh fungsi `calculateMatchScore()`.

---

## 4. Blueprint Struktur Kelas (Class Blueprint & Code Reference)

Berikut adalah struktur representasi kelas (*class diagram architecture*) dalam bentuk pseudocode terstruktur untuk memudahkan pembagian tugas pengerjaan modul pemrograman:

```java
// ==========================================
// CORE SYSTEM MODULE (Encapsulation & Composition)
// ==========================================

public class User {
    // Enkapsulasi: Menyembunyikan data sensitif
    private String userID;
    private String email;
    private String password;
    private boolean isVerified;
    
    // Komposisi: User memiliki satu MatchProfile secara utuh
    private MatchProfile matchProfile;

    public User(String userID, String email, String password) {
        this.userID = userID;
        this.email = email;
        this.password = password;
        this.isVerified = false; // default harus diverifikasi dulu
        this.matchProfile = new MatchProfile(); // Objek langsung di-instansiasi di dalam induk
    }

    // Getter & Setter untuk mengontrol akses data
    public boolean getIsVerified() {
        return this.isVerified;
    }

    public void verifyUser(String token) {
        // Logika verifikasi email kampus di sini
        if (token.equals("VALID_CAMPUS_TOKEN")) {
            this.isVerified = true;
        }
    }
}

public class MatchProfile {
    public String sleepSchedule;
    public String studyHabit;
    public String targetUniversity;
    private int matchScore; // Enkapsulasi: Tidak bisa diubah sembarangan dari luar

    public int getMatchScore() {
        return this.matchScore;
    }

    // Enkapsulasi Logika: Perhitungan skor kecocokan internal
    public void calculateMatchScore(MatchProfile otherProfile) {
        int score = 0;
        if (this.sleepSchedule.equals(otherProfile.sleepSchedule)) score += 40;
        if (this.studyHabit.equals(otherProfile.studyHabit)) score += 30;
        if (this.targetUniversity.equals(otherProfile.targetUniversity)) score += 30;
        this.matchScore = score;
    }
}

// ==========================================
// MARKETPLACE MODULE (Inheritance)
// ==========================================

// Base Class / Superclass
public class Listing {
    public String listingID;
    public String title;
    public String description;
    public User owner; // Asosiasi ke pemilik iklan

    public Listing(String listingID, String title, String description, User owner) {
        this.listingID = listingID;
        this.title = title;
        this.description = description;
        this.owner = owner;
    }
}

// Subclass untuk Iklan Tempat Tinggal (Meng-extend Listing)
public class HousingListing extends Listing {
    public double rentPrice;
    public String address;
    public int roomCount;

    public HousingListing(String listingID, String title, String description, User owner, double rentPrice, String address, int roomCount) {
        super(listingID, title, description, owner); // Memanggil constructor milik Base Class
        this.rentPrice = rentPrice;
        this.address = address;
        this.roomCount = roomCount;
    }
}

// Subclass untuk Iklan Barang / Buku (Meng-extend Listing)
public class ItemListing extends Listing {
    public double itemPrice;
    public String itemCondition;

    public ItemListing(String listingID, String title, String description, User owner, double itemPrice, String itemCondition) {
        super(listingID, title, description, owner); // Memanggil constructor milik Base Class
        this.itemPrice = itemPrice;
        this.itemCondition = itemCondition;
    }
}

// ==========================================
// COMMUNICATION MODULE (Composition)
// ==========================================

public class Group {
    public String groupID;
    public String groupName;
    
    // Komposisi: Grup memiliki daftar pesan. Jika grup dihapus, list ini hancur.
    private List<Message> chatHistory;

    public Group(String groupID, String groupName) {
        this.groupID = groupID;
        this.groupName = groupName;
        this.chatHistory = new ArrayList<Message>();
    }

    public void sendMessage(User sender, String content) {
        Message msg = new Message(sender, content, new Date().toString());
        this.chatHistory.add(msg);
    }

    public List<Message> getChatHistory() {
        return this.chatHistory;
    }
}

public class Message {
    public User sender;
    public String content;
    public String timestamp;

    public Message(User sender, String content, String timestamp) {
        this.sender = sender;
        this.content = content;
        this.timestamp = timestamp;
    }
}