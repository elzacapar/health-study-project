import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Definerar sökvägen till resultatmappen
RESULTS_PATH = 'results/'

class HealthAnalyzer:
    """
    En klass för att analysera hälsodata. 
    """

    def __init__(self, data_path):
        """
        Initialiserar analysatorn genom att ladda datasetet.
        """
        self.df = pd.read_csv(data_path)
        self.model = None 
        
    # --- Metoder flyttade från Del 1 ---

    def show_info(self):
        """Visar grundläggande info om datasetet."""
        print("--- Dataöversikt ---")
        print(self.df.head())
        print("\n--- Datainformation ---")
        print(self.df.info())

    def calculate_descriptive_stats(self):
        """
        Beräknar beskrivande statistik (medel, median, min, max).
        Motsvarar 'Beskrivande analys' från Del 1.
        """
        columns_to_analyze = ["age", "weight", "height", "systolic_bp", "cholesterol"]
        stats_df = self.df[columns_to_analyze].agg(["mean", "median", "min", "max"]).round(2)
        
        print("\n--- Deskriptiv Statistik ---")
        print(stats_df)
        return stats_df

    def plot_part1_visualizations(self):
        """
        Skapar de tre graferna från Del 1 i en och samma figur.
        1. Histogram (blodtryck)
        2. Boxplot (vikt vs kön)
        3. Barplot (rökare)
        """
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        plt.suptitle('Visualiseringar från Del 1', fontsize=16)

        # Graf 1: Histogram (blodtryck)
        sns.histplot(self.df['systolic_bp'], bins=20, kde=True, ax=axes[0])
        axes[0].set_title('Histogram: systoliskt BT')

        # Graf 2: Boxplot (vikt vs kön)
        sns.boxplot(x='sex', y='weight', data=self.df, ax=axes[1], 
                    hue='sex', palette={'M': 'skyblue', 'F': 'lightcoral'}, legend=False)
        axes[1].set_title('Boxplot: vikt per kön')

        # Graf 3: Barplot (rökare)
        smoker_counts = self.df['smoker'].value_counts(normalize=True) * 100
        smoker_series = pd.Series(smoker_counts.values, index=smoker_counts.index)
        
        sns.barplot(x=smoker_series.index, y=smoker_series.values, ax=axes[2], 
                    hue=smoker_series.index, palette=['green', 'red'], legend=False)
        
        axes[2].set_title('Andel rökare (%)')
        axes[2].set_ylabel('Procent')
        
        for i, val in enumerate(smoker_counts.values):
             axes[2].text(i, val + 0.5, f'{val:.1f}%', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(f'{RESULTS_PATH}part1_visualizations.png')
        plt.show()

    def test_smoker_hypothesis(self):
        """
        Testar hypotesen: rökare har högre blodtryck än icke-rökare.
        (Welch's t-test).
        """
        bp_smoker = self.df[self.df['smoker'] == 'Yes']['systolic_bp']
        bp_non = self.df[self.df['smoker'] == 'No']['systolic_bp']

        # Utför t-test
        t_stat, p_two = stats.ttest_ind(bp_smoker, bp_non, equal_var=False)
        
        # Ensidigt p-värde (om t-stat > 0 delar vi med 2)
        if t_stat > 0:
            p_one = p_two / 2
        else:
            p_one = 1.0

        print("\n--- Hypotesprövning (Rökare vs BT) ---")
        print(f"Medelvärde rökare: {bp_smoker.mean():.2f}")
        print(f"Medelvärde icke-rökare: {bp_non.mean():.2f}")
        print(f"T-statistik: {t_stat:.4f}")
        print(f"P-värde (ensidigt): {p_one:.4f}")
        
        if p_one < 0.05:
            print("Slutsats: signifikant skillnad (förkasta H0).")
        else:
            print("Slutsats: ingen signifikant skillnad (behåll H0).")


    # --- Metoder för Del 2 ---

    def plot_correlation_matrix(self):
        """Ritar korrelationsmatris."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Korrelationsmatris")
        plt.savefig(f'{RESULTS_PATH}correlation_matrix.png')
        plt.show()

    def perform_regression(self, feature_cols, target_col='systolic_bp'):
        """
        Kör linjär regression (enkel eller multipel) med scikit-learn.
        """
        X = self.df[feature_cols]
        y = self.df[target_col]

        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        
        r2 = r2_score(y, y_pred)
        mse = mean_squared_error(y, y_pred)

        print(f"\n--- Regression (features: {feature_cols}) ---")
        print(f"R²: {r2:.4f}")
        print(f"MSE: {mse:.4f}")
        print(f"Intercept: {model.intercept_:.4f}")
        for col, coef in zip(feature_cols, model.coef_):
            print(f"Koefficient ({col}): {coef:.4f}")

        # Plotta endast om det är enkel regression
        if len(feature_cols) == 1:
            plt.figure(figsize=(8, 5))
            plt.scatter(X.iloc[:,0], y, alpha=0.5, label='Data')
            plt.plot(X.iloc[:,0], y_pred, color='red', label='Regressionslinje')
            plt.title(f"Regression: {feature_cols[0]} -> {target_col}")
            plt.legend()
            plt.savefig(f'{RESULTS_PATH}simple_regression.png')
            plt.show()

    def test_disease_proportion(self, group_col='sex', target_value=1):
        """
        Utökad analys: proportionstest för sjukdomsförekomst mellan grupper. Testar om andelen individer med sjukdomen (disease=1) skiljer sig
        mellan de två största grupperna i en given kategorisk kolumn.
        """
        groups = self.df[group_col].value_counts().index.tolist()
        if len(groups) < 2:
            print("Fel: Kolumnen måste ha minst två kategorier för jämförelse.")
            return

        g1, g2 = groups[0], groups[1]

        df_g1 = self.df[self.df[group_col] == g1]
        df_g2 = self.df[self.df[group_col] == g2]
        
        # Antal sjuka och totalt antal per grupp
        count = [
            (df_g1['disease'] == target_value).sum(),
            (df_g2['disease'] == target_value).sum()
        ]
        nobs = [
            len(df_g1),
            len(df_g2)
        ]

        # Utför z-test för två andelar (statsmodels)
        stat, pval = proportions_ztest(count, nobs)
        
        p1 = count[0] / nobs[0]
        p2 = count[1] / nobs[1]
        
        print(f"\n--- Proportionstest: Sjukdomsfrekvens ({group_col}: {g1} vs {g2}) ---")
        print(f"Andel sjuka {g1}: {count[0]}/{nobs[0]} ({p1:.2%})")
        print(f"Andel sjuka {g2}: {count[1]}/{nobs[1]} ({p2:.2%})")
        print(f"Skillnad ({g1} - {g2}): {(p1 - p2):.3f} i andel")
        print(f"Z-statistik: {stat:.4f}")
        print(f"Tvåsidigt P-värde: {pval:.4f}")
        
        if pval < 0.05:
            print("Slutsats: Det finns en signifikant skillnad i sjukdomsfrekvens.")
        else:
            print("Slutsats: Ingen signifikant skillnad påvisades.")

        # Visualisering (Bar plot)
        proportions = pd.DataFrame({
            group_col: [g1, g2],
            'Disease Rate': [p1, p2]
        })
        
        plt.figure(figsize=(6, 4))
        sns.barplot(x=group_col, y='Disease Rate', data=proportions, 
            hue=group_col, palette={'F': 'lightcoral', 'M': 'skyblue'}, legend=False)
        plt.title(f"Sjukdomsförekomst efter {group_col}")
        plt.ylabel("Andel sjuka")
        plt.ylim(0, max(p1, p2) * 1.2)
        plt.savefig(f'{RESULTS_PATH}disease_proportion.png')
        plt.show()